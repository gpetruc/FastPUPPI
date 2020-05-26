// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/L1THGCal/interface/HGCalCluster.h"
#include "DataFormats/L1THGCal/interface/HGCalMulticluster.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"


class HGCalUnclustered : public edm::stream::EDProducer<>  {
    public:
        explicit HGCalUnclustered(const edm::ParameterSet&);
        ~HGCalUnclustered();

        void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override;

    private:
        edm::EDGetTokenT<l1t::HGCalClusterBxCollection> src2D_;
        edm::EDGetTokenT<l1t::HGCalMulticlusterBxCollection> src3D_;
        StringCutObjectSelector<l1t::HGCalMulticluster> sel_;
};

HGCalUnclustered::HGCalUnclustered(const edm::ParameterSet& iConfig) :
    src2D_(consumes<l1t::HGCalClusterBxCollection>(iConfig.getParameter<edm::InputTag>("src2D"))),
    src3D_(consumes<l1t::HGCalMulticlusterBxCollection>(iConfig.getParameter<edm::InputTag>("src3D"))),
    sel_(iConfig.getParameter<std::string>("cut"))
{

    produces<l1t::HGCalClusterBxCollection>();
 }

HGCalUnclustered::~HGCalUnclustered() { }

// ------------ method called for each event  ------------
void
HGCalUnclustered::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    // Output collections
    auto out = std::make_unique<l1t::HGCalClusterBxCollection>();

    // Input collections
    edm::Handle<l1t::HGCalMulticlusterBxCollection> src3D;
    edm::Handle<l1t::HGCalClusterBxCollection> src2D;
    iEvent.getByToken(src3D_, src3D);
    iEvent.getByToken(src2D_, src2D);

    std::vector<bool> used(src2D->size());
    bool first = true;
    for (const auto & c3D : *src3D) {
        if (sel_(c3D)) {
            for (const auto & pair : c3D.constituents()) {
                if (first) { 
                    if (src2D.id() != pair.second.id()) throw cms::Exception("Configuration", "Mismatch between 2D and 3D cluster inputs");
                    first = false;  // waste of time to do it always
                }
                used[pair.second.key()] = true;
            }
        }
    }

    unsigned int i = 0;
    for (auto it = src2D->begin(), ed = src2D->end(); it != ed; ++it, ++i) {
        if (!used[i]) out->push_back(0, *it);
    }

    iEvent.put(std::move(out));

 }

//define this as a plug-in
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(HGCalUnclustered);
