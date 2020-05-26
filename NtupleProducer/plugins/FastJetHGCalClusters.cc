// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/L1THGCal/interface/HGCalTriggerCell.h"
#include "DataFormats/L1THGCal/interface/HGCalCluster.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "fastjet/ClusterSequence.hh"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "L1Trigger/L1THGCal/interface/backend/HGCalShowerShape.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"


class FastJetHGCalClusters : public edm::stream::EDProducer<>  {
    public:
        explicit FastJetHGCalClusters(const edm::ParameterSet&);
        ~FastJetHGCalClusters();

        void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override;

    private:
        edm::EDGetTokenT<l1t::HGCalClusterBxCollection> src_;
        fastjet::JetDefinition jetDef_;
        double ptMin_;
        StringCutObjectSelector<l1t::HGCalMulticluster> sel_;

        // tools
        edm::ESHandle<HGCalTriggerGeometryBase> triggerGeometry_;
        HGCalShowerShape shape_;


};

FastJetHGCalClusters::FastJetHGCalClusters(const edm::ParameterSet& iConfig) :
    src_(consumes<l1t::HGCalClusterBxCollection>(iConfig.getParameter<edm::InputTag>("src"))),
    ptMin_(iConfig.getParameter<double>("ptMin")),
    sel_(iConfig.getParameter<std::string>("cut")),
    shape_(iConfig)
{
    std::string algo = iConfig.getParameter<std::string>("algo");
    if (algo == "anti-kt") {
        jetDef_ = fastjet::JetDefinition(fastjet::antikt_algorithm, iConfig.getParameter<double>("R"));
    } else {
        throw cms::Exception("Configuration", "Unsupported algorithm: "+algo);
    }

    produces<l1t::HGCalMulticlusterBxCollection>();
 }

FastJetHGCalClusters::~FastJetHGCalClusters() { }

// ------------ method called for each event  ------------
void
FastJetHGCalClusters::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // init geometry etc
    shape_.eventSetup(iSetup);
    iSetup.get<CaloGeometryRecord>().get("", triggerGeometry_);


    // Output collections
    auto out = std::make_unique<l1t::HGCalMulticlusterBxCollection>();

    // Input collections
    edm::Handle<l1t::HGCalClusterBxCollection> src;
    iEvent.getByToken(src_, src);

    std::vector<fastjet::PseudoJet> inputs;
    unsigned int i = 0;
    for (const auto & c2d : *src) {
        inputs.emplace_back(c2d.px(), c2d.py(), c2d.pz(), c2d.energy());
        inputs.back().set_user_index(i++);
    }
 
    fastjet::ClusterSequence cs(inputs, jetDef_);
    vector<fastjet::PseudoJet> jets = cs.inclusive_jets(ptMin_);
    for (const auto & jet : jets) {
        l1t::HGCalMulticluster c3d;
        for (const auto & constit : jet.constituents()) {
            c3d.addConstituent(edm::Ptr<l1t::HGCalCluster>(src, constit.user_index()));
        }
        c3d.saveHOverE();
        shape_.fillShapes(c3d, *triggerGeometry_);
        if (sel_(c3d)) {
            out->push_back(0, c3d);
            continue;
        }
    }

    iEvent.put(std::move(out));

 }

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(FastJetHGCalClusters);
