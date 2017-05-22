import FWCore.ParameterSet.Config as cms

EmOut = cms.EDProducer('GetEMPart',
        src = cms.InputTag('l1tPFHGCalProducerFrom3DTPs'),
)	
