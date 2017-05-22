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

process.ntuple = cms.EDAnalyzer("ResponseNTuplizer",
    genJets = cms.InputTag("ak4GenJetsNoNu"),
    genParticles = cms.InputTag("genParticles"),
    isParticleGun = cms.bool(False),
    objects = cms.PSet(
        # -- offline inputs --
        Ecal = cms.VInputTag('l1tPFEcalProducerFromOfflineRechits:towers','l1tPFHGCalEEProducerFromOfflineRechits:towers', 'l1tPFHFProducerFromOfflineRechits:towers'),
        Hcal = cms.VInputTag('l1tPFHcalProducerFromOfflineRechits:towers','l1tPFHGCalFHProducerFromOfflineRechits:towers', 'l1tPFHGCalBHProducerFromOfflineRechits:towers', 'l1tPFHFProducerFromOfflineRechits:towers'),
        Calo = cms.VInputTag('l1tPFEcalProducerFromOfflineRechits:towers','l1tPFHGCalEEProducerFromOfflineRechits:towers', 'l1tPFHcalProducerFromOfflineRechits:towers', 'l1tPFHGCalFHProducerFromOfflineRechits:towers', 'l1tPFHGCalBHProducerFromOfflineRechits:towers', 'l1tPFHFProducerFromOfflineRechits:towers'),
        TK   = cms.VInputTag('l1tPFTkProducersFromOfflineTracksStrips'),
        # -- TP inputs --
        #TPEcal = cms.VInputTag('l1tPFEcalProducerFromTPDigis:towers','l1tPFHGCalProducerFromTriggerCells:towersEE',),
        #TPHcal = cms.VInputTag('l1tPFHcalProducerFromTPDigis','l1tPFHGCalProducerFromTriggerCells:towersFHBH',),
        #TPTK   = cms.VInputTag('l1tPFTkProducersFromL1Tracks',),
        # -- processed --
        L1RawCalo = cms.VInputTag("InfoOut:RawCalo",),
        L1Calo = cms.VInputTag("InfoOut:Calo",),
        L1TK = cms.VInputTag("InfoOut:TK",),
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
process.p = cms.Path(process.ntuple)
process.TFileService = cms.Service("TFileService", fileName = cms.string("respTupleNew.root"))


if True:
    process.load('FastPUPPI.NtupleProducer.caloNtupleProducer_cfi')
    process.load('FastPUPPI.NtupleProducer.ntupleProducer_cfi')
    process.load('FastPUPPI.NtupleProducer.l1tPFMuProducerFromL1Mu_cfi')
    process.load('FastPUPPI.NtupleProducer.emFractionProducer_cfi')
    process.CaloInfoOut.outputName = ""; # turn off Ntuples
    process.InfoOut.outputName = ""; # turn off Ntuples
    process.p = cms.Path(process.EmOut + process.CaloInfoOut + process.InfoOut + process.ntuple)
    #process.p = cms.Path(process.EmOut + process.InfoOut + process.ntuple)
def goGun():
    process.ntuple.isParticleGun = True
def goSpring17(mode="towers"):
    del process.ntuple.objects.TK
    process.ntuple.objects.TPTK   = cms.VInputTag('l1tPFTkProducersFromL1Tracks',)
    if hasattr(process, 'InfoOut'):
        process.InfoOut.L1TrackTag = 'l1tPFTkProducersFromL1Tracks'
    if mode == "towers":
        process.ntuple.objects.TPEcal = cms.VInputTag('l1tPFEcalProducerFromTPDigis:towers', 'l1tPFHGCalProducerFromTriggerCells:towersEE',)
        process.ntuple.objects.TPHcal = cms.VInputTag('l1tPFHcalProducerFromTPDigis', 'l1tPFHGCalProducerFromTriggerCells:towersFHBH',)
        process.ntuple.objects.TPCalo = cms.VInputTag('l1tPFEcalProducerFromTPDigis:towers', 'l1tPFHGCalProducerFromTriggerCells:towersEE', 'l1tPFHcalProducerFromTPDigis', 'l1tPFHGCalProducerFromTriggerCells:towersFHBH',)
        if hasattr(process, 'InfoOut'):
            process.CaloInfoOut.EcalTPTags = [ 'l1tPFEcalProducerFromTPDigis:towers', 'l1tPFHGCalProducerFromTriggerCells:towersEE' ]
            process.CaloInfoOut.HcalTPTags = [ 'l1tPFHcalProducerFromTPDigis', 'l1tPFHGCalProducerFromTriggerCells:towersFHBH', ]
            process.CaloInfoOut.caloClusterer.linker.useCorrectedEcal = False
            #process.CaloInfoOut.corrector   = cms.string("/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_9_1_0_pre3/src/FastPUPPI/NtupleProducer/data/pion_eta_phi.root")
            #process.CaloInfoOut.ecorrector  = cms.string("/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_9_1_0_pre3/src/FastPUPPI/NtupleProducer/data/ecorr.root")
            # Temporary calibrations
            if True:
                process.CaloInfoOut.caloClusterer.linker.useCorrectedEcal = True
                process.CaloInfoOut.simpleCorrEM = cms.PSet(
			etaBins = cms.vdouble( 0.500,  1.000,  1.500,  2.000,  2.500,  3.000),
			offset  = cms.vdouble(-2.245, -2.555, -2.767, -1.654, -1.875, -2.092),
			scale   = cms.vdouble( 0.961,  0.967,  0.949,  0.875,  0.914,  0.951),
                )
                process.CaloInfoOut.simpleCorrHad = cms.PSet(
			etaBins = cms.vdouble( 0.500,  0.500,  0.500,  1.000,  1.000,  1.000,  1.500,  1.500,  1.500,  2.000,  2.000,  2.000,  2.500,  2.500,  2.500,  3.000,  3.000,  3.000,  3.500,  4.000,  4.500,  5.000),
			emfBins = cms.vdouble( 0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  0.125,  0.500,  0.875,  1.100,  1.100,  1.100,  1.100),
			offset  = cms.vdouble(-3.826,  2.359, -2.084, -4.482,  1.154, -2.041, -3.064,  1.938, -0.633, -1.115,  1.414, -0.805, -3.006,  0.646, -1.882, -2.187,  2.588, -1.457, -5.611, -5.885, -4.012, -2.391),
			scale   = cms.vdouble( 0.977,  0.658,  0.696,  1.002,  0.668,  0.696,  0.914,  0.646,  0.626,  0.591,  0.632,  0.700,  0.644,  0.632,  0.722,  0.579,  0.538,  0.657,  2.306,  2.295,  2.092,  1.447),
                )
            # Temporary resolutions
            if True:
                process.InfoOut.simpleResolHad = cms.PSet(
                        etaBins = cms.vdouble( 1.300,  1.700,  2.800,  3.200,  4.000,  5.000),
                        offset  = cms.vdouble( 3.522,  0.078,  2.071,  1.708,  1.148, -0.265),
                        scale   = cms.vdouble( 0.124,  0.494,  0.183,  0.257,  0.162,  0.428),
                        kind    = cms.string('calo'),
                        )
                process.InfoOut.simpleResolEm = cms.PSet(
                        etaBins = cms.vdouble( 1.300,  1.700,  2.800,  3.200,  4.000,  5.000),
                        offset  = cms.vdouble( 0.849,  0.626,  0.157, -1.305,  0.607, -3.985),
                        scale   = cms.vdouble( 0.016,  0.097,  0.043,  0.305,  0.142,  0.626),
                        kind    = cms.string('calo'),
                        )
                process.InfoOut.simpleResolTrk  = cms.PSet(
                        etaBins = cms.vdouble( 0.800,  1.200,  1.500,  2.000,  2.500),
                        offset  = cms.vdouble( 0.006,  0.010,  0.010,  0.019,  0.027),
                        scale   = cms.vdouble( 0.303,  0.465,  1.003,  1.219,  1.518),
                        kind    = cms.string('track'),
                        )
            # Options to optimize the linking
            if True:
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
    else:
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
            if True:
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
	    if False:			
                process.CaloInfoOut.caloClusterer.linker.useCorrectedEcal = True
                process.CaloInfoOut.corrector = cms.string('FastPUPPI/NtupleProducer/data/pion_eta_phi.root')
		process.CaloInfoOut.ecorrector = cms.string('FastPUPPI/NtupleProducer/data/ecorr.root')
		
            process.InfoOut.CaloClusterTags = [ cms.InputTag('CaloInfoOut','calibrated') ]
	    process.InfoOut.correctCaloEnergies = cms.bool(False)
	    if False:			
                process.InfoOut.corrector = cms.string('FastPUPPI/NtupleProducer/data/pion_eta_phi.root')
		process.InfoOut.ecorrector = cms.string('FastPUPPI/NtupleProducer/data/ecorr.root')
		process.InfoOut.eleres = cms.string('FastPUPPI/NtupleProducer/data/eres.root')
		process.InfoOut.pionres = cms.string('FastPUPPI/NtupleProducer/data/pionres.root')
		process.InfoOut.trackres = cms.string('FastPUPPI/NtupleProducer/data/tkres.root')		
            if True:
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
            if True:
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
        process.p = cms.Path(process.InfoOut + process.InfoOutReg + process.ntuple)
    else:
        process.InfoOut.regions = regions
if False:
    process.out = cms.OutputModule("PoolOutputModule",
            fileName = cms.untracked.string("l1pf_remade.root"),
    )
    process.e = cms.EndPath(process.out)
if False:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.maxEvents.input = 3
    process.InfoOut.debug = 2
    if False:
        process.filter = cms.EDFilter("CandViewSelector",
            src = cms.InputTag("genParticles"),
            cut = cms.string("pt > 10 && abs(eta) < 1.5"),
            filter = cms.bool(True),
        )
        process.p = cms.Path(process.filter + process.InfoOut)

goGun()
goSpring17("")
