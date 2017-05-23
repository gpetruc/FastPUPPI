import FWCore.ParameterSet.Config as cms

process = cms.Process("RESP")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True), allowUnscheduled = cms.untracked.bool(False) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/eos/cms/store/cmst3/user/gpetrucc/l1phase2/Spring17D/090517/inputs_17D_SinglePion_NoPU_job12.root')
)
process.source.duplicateCheckMode = cms.untracked.string("noDuplicateCheck")


process.load('FastPUPPI.NtupleProducer.caloNtupleProducer_cfi')
process.load('FastPUPPI.NtupleProducer.ntupleProducer_cfi')
process.CaloInfoOut.outputName = ""; # turn off Ntuples
process.InfoOut.outputName = ""; # turn off Ntuples

process.ntuple = cms.EDAnalyzer("ResponseNTuplizer",
    genJets = cms.InputTag("ak4GenJetsNoNu"),
    genParticles = cms.InputTag("genParticles"),
    isParticleGun = cms.bool(False),
    doRandom = cms.bool(False),
    objects = cms.PSet(
        # -- offline inputs --
        Ecal = cms.VInputTag('l1tPFEcalProducerFromOfflineRechits:towers','l1tPFHGCalEEProducerFromOfflineRechits:towers', 'l1tPFHFProducerFromOfflineRechits:towers'),
        Hcal = cms.VInputTag('l1tPFHcalProducerFromOfflineRechits:towers','l1tPFHGCalFHProducerFromOfflineRechits:towers', 'l1tPFHGCalBHProducerFromOfflineRechits:towers', 'l1tPFHFProducerFromOfflineRechits:towers'),
        Calo = cms.VInputTag('l1tPFEcalProducerFromOfflineRechits:towers','l1tPFHGCalEEProducerFromOfflineRechits:towers', 'l1tPFHcalProducerFromOfflineRechits:towers', 'l1tPFHGCalFHProducerFromOfflineRechits:towers', 'l1tPFHGCalBHProducerFromOfflineRechits:towers', 'l1tPFHFProducerFromOfflineRechits:towers'),
        #TK   = cms.VInputTag('l1tPFTkProducersFromOfflineTracksStrips'),
        # -- TP inputs --
        TPEcal = cms.VInputTag('l1tPFEcalProducerFromTPDigis:towers','l1tPFHGCalProducerFromTriggerCells:towersEE',),
        TPHcal = cms.VInputTag('l1tPFHcalProducerFromTPDigis','l1tPFHGCalProducerFromTriggerCells:towersFHBH',),
        TPCalo = cms.VInputTag('l1tPFEcalProducerFromTPDigis:towers', 'l1tPFHGCalProducerFromTriggerCells:towersEE', 'l1tPFHcalProducerFromTPDigis', 'l1tPFHGCalProducerFromTriggerCells:towersFHBH',),
        TPTK   = cms.VInputTag('l1tPFTkProducersFromL1Tracks',),
        # -- processed --
        L1RawEcal = cms.VInputTag(cms.InputTag('CaloInfoOut','emUncalibrated')),
        L1Ecal = cms.VInputTag(cms.InputTag('CaloInfoOut','emCalibrated')),
        L1RawCalo = cms.VInputTag(cms.InputTag('CaloInfoOut','uncalibrated')),
        L1Calo = cms.VInputTag("InfoOut:Calo",),
        L1TK = cms.VInputTag("InfoOut:TK",),
        L1TKV = cms.VInputTag("InfoOut:TKVtx",),
        L1PF = cms.VInputTag("InfoOut:PF",),
        L1Puppi = cms.VInputTag("InfoOut:Puppi",),
        # -- processed (integer math) --
        L1ICalo = cms.VInputTag("InfoOut:L1Calo",),
        L1ITK = cms.VInputTag("InfoOut:L1TK",),
        L1IPF = cms.VInputTag("InfoOut:L1PF",),
        L1IPuppi = cms.VInputTag("InfoOut:L1Puppi",),
       ## -- clustered --
       #L1ak4RawCalo = cms.VInputTag("ak4L1RawCalo",),
       #L1ak4Calo = cms.VInputTag("ak4L1Calo",),
       #L1ak4TK = cms.VInputTag("ak4L1TK",),
       #L1ak4PF = cms.VInputTag("ak4L1PF",),
       #L1ak4Puppi = cms.VInputTag("ak4L1Puppi",),
    ),
    copyUInts = cms.VInputTag(
        "InfoOut:totNL1Calo", "InfoOut:totNL1TK", "InfoOut:totNL1Mu", "InfoOut:totNL1PF", "InfoOut:totNL1Puppi",
        "InfoOut:maxNL1Calo", "InfoOut:maxNL1TK", "InfoOut:maxNL1Mu", "InfoOut:maxNL1PF", "InfoOut:maxNL1Puppi",
    )
)
process.p = cms.Path(process.CaloInfoOut + process.InfoOut + process.ntuple)
process.TFileService = cms.Service("TFileService", fileName = cms.string("respTupleNew.root"))

# Below for more debugging
if True:
    process.genInAcceptance = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("status == 1 && (abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16) && "+
                         "(abs(eta) < 2.5 && pt > 2 && charge != 0 || "+
                         "abs(pdgId) == 22 && pt > 1 || "+
                         "charge == 0 && pt > 1 || "+
                         "charge != 0 && abs(eta) > 2.5 && pt > 2) ") # tracks below pT 2 bend by more than 0.4,
    )
    process.ntuple.objects.GenAcc = cms.VInputTag(cms.InputTag("genInAcceptance"))
    process.chGenInAcceptance = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("status == 1 && (abs(eta) < 2.5 && pt > 2 && charge != 0)")
    )
    process.phGenInAcceptance = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("status == 1 && pt > 1 && pdgId == 22")
    )
    process.ntuple.objects.ChGenAcc = cms.VInputTag(cms.InputTag("chGenInAcceptance"))
    process.ntuple.objects.PhGenAcc = cms.VInputTag(cms.InputTag("phGenInAcceptance"))
    process.p = cms.Path(process.genInAcceptance + process.chGenInAcceptance + process.phGenInAcceptance + process.p._seq)
    process.L1PFCharged  = cms.EDFilter("CandViewSelector", src = cms.InputTag("InfoOut:PF"),   cut = cms.string("charge != 0"))
    process.L1IPFCharged = cms.EDFilter("CandViewSelector", src = cms.InputTag("InfoOut:L1PF"), cut = cms.string("charge != 0"))
    process.L1PFPhoton  = cms.EDFilter("CandViewSelector", src = cms.InputTag("InfoOut:PF"),   cut = cms.string("pdgId == 22"))
    process.L1IPFPhoton = cms.EDFilter("CandViewSelector", src = cms.InputTag("InfoOut:L1PF"), cut = cms.string("pdgId == 22"))
    process.ntuple.objects.L1PFCharged = cms.VInputTag("L1PFCharged",)
    process.ntuple.objects.L1IPFCharged = cms.VInputTag("L1IPFCharged",)
    process.ntuple.objects.L1PFPhoton = cms.VInputTag("L1PFPhoton",)
    process.ntuple.objects.L1IPFPhoton = cms.VInputTag("L1IPFPhoton",)
    process.p.replace(process.ntuple, process.L1PFCharged + process.L1IPFCharged + process.L1PFPhoton + process.L1IPFPhoton + process.ntuple)

def goGun():
    process.ntuple.isParticleGun = True
def useClusters():
        process.EmOut.src = cms.InputTag('l1tPFHGCalProducerFrom3DTPs')
        process.ntuple.objects.TPEcal = cms.VInputTag( 'l1tPFEcalProducerFromL1EGCrystalClusters', cms.InputTag('EmOut') )
        process.ntuple.objects.TPHcal = cms.VInputTag( 'l1tPFHcalProducerFromTPDigis', 'l1tPFHGCalProducerFromTriggerCells:towersFHBH', 'l1tPFHFProducerFromOfflineRechits:towers')
        process.ntuple.objects.TPCalo = cms.VInputTag( 'l1tPFEcalProducerFromL1EGCrystalClusters', cms.InputTag('EmOut'), 'l1tPFHcalProducerFromTPDigis', 'l1tPFHGCalProducerFromTriggerCells:towersFHBH', 'l1tPFHFProducerFromOfflineRechits:towers' )
        if hasattr(process, 'InfoOut'):
            process.CaloInfoOut.EcalTPTags = [ 'l1tPFEcalProducerFromL1EGCrystalClusters', cms.InputTag('EmOut') ]
            process.CaloInfoOut.HcalTPTags = [ 'l1tPFHcalProducerFromTPDigis', 'l1tPFHGCalProducerFromTriggerCells:towersFHBH', 'l1tPFHFProducerFromOfflineRechits:towers' ]
	          process.CaloInfoOut.outputName = cms.untracked.string('ntuple.root')
	          process.CaloInfoOut.zeroSuppress = cms.bool(True)
	          process.CaloInfoOut.caloClusterer.linker.useCorrectedEcal = False
            if True: #use Giovanni's simple corrections
                process.CaloInfoOut.caloClusterer.linker.useCorrectedEcal = True
                process.CaloInfoOut.simpleCorrEM = cms.PSet( 
			                  etaBins = cms.vdouble( 0.500,  1.000,  1.500,  2.000,  2.500,  3.000),
			                  offset  = cms.vdouble(-2.245, -2.555, -2.767, -1.654, -1.875, -2.092),
			                  scale   = cms.vdouble( 0.961,  0.967,  0.949,  0.875,  0.914,  0.951),
                )
                process.CaloInfoOut.simpleCorrHad = cms.PSet(
			                  etaBins = cms.vdouble( 0.500,  0.500,  0.500,  1.000,  1.000,  1.000,  1.500,  1.500,  1.500,  2.000,  2.000,  2.000,  2.500,  2.500,  2.500,  3.000,  3.000,  3.000,  3.500,  4.000,  4.500,  5.000),
			                  emfBins = cms.vdouble( 0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  1.100,  1.100,  1.100,  1.100),
			                  offset  = cms.vdouble(-3.826,  2.359, -2.084, -4.482,  1.154, -2.041, -3.064,  1.938, -0.633, -1.115,  1.414, -0.805, -3.006,  0.646, -1.882, -2.187,  2.594, -1.450, -5.611, -5.885, -4.012, -2.391),
			                  scale   = cms.vdouble( 0.977,  0.658,  0.696,  1.002,  0.668,  0.696,  0.914,  0.646,  0.626,  0.591,  0.632,  0.700,  0.644,  0.632,  0.722,  0.579,  0.538,  0.657,  2.306,  2.295,  2.092,  1.447),
                )			    	    
	          if False: #use Phil's corrections			
                process.CaloInfoOut.caloClusterer.linker.useCorrectedEcal = True
                process.CaloInfoOut.corrector = cms.string('FastPUPPI/NtupleProducer/data/pion_eta_phi.root')
		            process.CaloInfoOut.ecorrector = cms.string('FastPUPPI/NtupleProducer/data/ecorr.root')
		
            process.InfoOut.CaloClusterTags = [ cms.InputTag('CaloInfoOut','calibrated') ]
	          process.InfoOut.correctCaloEnergies = cms.bool(False)
	          if False:	#use Phil's corrections		
                process.InfoOut.corrector = cms.string('FastPUPPI/NtupleProducer/data/pion_eta_phi.root')
		            process.InfoOut.ecorrector = cms.string('FastPUPPI/NtupleProducer/data/ecorr.root')
		            process.InfoOut.eleres = cms.string('FastPUPPI/NtupleProducer/data/eres.root')
		            process.InfoOut.pionres = cms.string('FastPUPPI/NtupleProducer/data/pionres.root')
		            process.InfoOut.trackres = cms.string('FastPUPPI/NtupleProducer/data/tkres.root')		
            if True: #use Giovanni's simple corrections
                process.InfoOut.simpleResolHad = cms.PSet(
			                  etaBins = cms.vdouble( 1.300,  1.700,  2.800,  3.200,  4.000,  5.000),
			                  offset  = cms.vdouble( 3.074,  0.113,  2.110,  1.510,  1.098, -0.065),
			                  scale   = cms.vdouble( 0.137,  0.514,  0.194,  0.266,  0.162,  0.324),
			                  kind    = cms.string('calo'),
                )
                process.InfoOut.simpleResolEm = cms.PSet(
			                  etaBins = cms.vdouble( 1.300,  1.700,  2.800,  3.200,  4.000,  5.000),
			                  offset  = cms.vdouble( 1.038,  0.697,  0.605, -1.308,  0.668, -0.097),
			                  scale   = cms.vdouble( 0.015,  0.114,  0.037,  0.622,  0.149,  0.313),
			                  kind    = cms.string('calo'),
                )
                process.InfoOut.simpleResolTrk  = cms.PSet(
			                  etaBins = cms.vdouble( 0.800,  1.200,  1.500,  2.000,  2.500),
			                  offset  = cms.vdouble( 0.005,  0.008,  0.003,  0.018,  0.022),
			                  scale   = cms.vdouble( 0.302,  0.503,  1.133,  1.215,  1.712),
			                  kind    = cms.string('track'),
                )
                if True: #optimize linking
                    process.InfoOut.linking = cms.PSet(
                            trackCaloDR = cms.double(0.15),
                            trackCaloNSigmaLow = cms.double(2.0),
                            trackCaloNSigmaHigh = cms.double(2.0),
                            useTrackCaloSigma = cms.bool(True),
                            rescaleUnmatchedTrack = cms.bool(False),
                            maxInvisiblePt = cms.double(20.0),
                    )			
						    
                process.ntuple.objects.L1RawCalo = cms.VInputTag(cms.InputTag('CaloInfoOut','uncalibrated'))
                process.ntuple.objects.L1RawEcal = cms.VInputTag(cms.InputTag('CaloInfoOut','emUncalibrated'))
                process.ntuple.objects.L1Ecal = cms.VInputTag(cms.InputTag('CaloInfoOut','emCalibrated'))
	              process.ntuple.objects.L1Calo = cms.VInputTag("InfoOut:Calo")
      
def goRegional(inParallel=False):
    regions = cms.VPSet(
            cms.PSet(
                etaBoundaries = cms.vdouble(-5.5,-4,-3),
                phiSlices = cms.uint32(4),
                etaExtra = cms.double(0.2),
                phiExtra = cms.double(0.2),
            ),
            cms.PSet(
                etaBoundaries = cms.vdouble(-3,-1.5,0,1.5,3),
                phiSlices = cms.uint32(6),
                etaExtra = cms.double(0.2),
                phiExtra = cms.double(0.2),
            ),
            cms.PSet(
                etaBoundaries = cms.vdouble(3,4,5.5),
                phiSlices = cms.uint32(4),
                etaExtra = cms.double(0.2),
                phiExtra = cms.double(0.2),
            ),
    )
    if inParallel:
        process.InfoOutReg = process.InfoOut.clone(regions = regions)
        process.p = cms.Path(process.CaloInfoOut + process.InfoOut + process.InfoOutReg + process.ntuple)
    else:
        process.InfoOut.regions = regions
if False:
    #goGun(); 
    tmpCalib(); tmpResol(); newLink();
    #process.source.fileNames = ['/store/cmst3/user/gpetrucc/l1phase2/Spring17D/010517/inputs_17D_SinglePion0_NoPU_job42.root']
    #process.source.fileNames = ['/store/cmst3/user/gpetrucc/l1phase2/Spring17D/010517/inputs_17D_SinglePion_NoPU_job42.root']
    process.source.fileNames = ['/store/cmst3/user/gpetrucc/l1phase2/Spring17D/010517/inputs_17D_TTbar_NoPU_job1.root']
    process.out = cms.OutputModule("PoolOutputModule",
            fileName = cms.untracked.string("l1pf_remade.root"),
    )
    process.e = cms.EndPath(process.out)
    process.maxEvents.input = 50
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    if False:
        #process.source.fileNames = [ 'file:l1pf_remade.root' ]
        process.TFileService.fileName = cms.string("respTupleNew_1.root")
        process.out.fileName = cms.untracked.string("l1pf_remade_1.root")
        process.source.eventsToProcess = cms.untracked.VEventRange("1:6315:307280")
process.InfoOut.debug = 1
