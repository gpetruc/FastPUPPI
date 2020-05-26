#!/bin/bash

V="110X_v0.2"
PLOTDIR="plots/11_1_X/from110X/${V}/"
SAMPLES="--110X_v0_fat";

W=$1; shift;
case $W in
    run-pu0)
         for X in MultiPion_PT0to200 DoublePhoton_FlatPt-1To100; do 
            ./scripts/prun.sh runPerformanceNTuple.py $SAMPLES ${X}_PU0 ${X}_PU0.${V} --inline-customize 'goGun();noPU();testHGC()'; 
         done
         ;;
    run-pu200)
         for X in SinglePion_PT0to200 DoublePhoton_FlatPt-1To100; do 
             ./scripts/prun.sh runPerformanceNTuple.py $SAMPLES ${X}_PU200 ${X}_PU200.${V} --inline-customize 'goGun();noPU();testHGC();goMT()'; 
         done
         ;;
    run-jets0)
         for X in TTbar; do 
            ./scripts/prun.sh runPerformanceNTuple.py $SAMPLES ${X}_PU0 ${X}_PU0.${V} --inline-customize 'addCalib();respOnly();noPU();testHGC()'; 
         done
         ;;
    run-jets200)
         for X in TTbar; do 
            ./scripts/prun.sh runPerformanceNTuple.py $SAMPLES ${X}_PU200 ${X}_PU200.${V} --inline-customize 'addCalib();respOnly();noPU();testHGC()'; 
         done
         ;;

    hgc-calib)
         NTUPLES=$(ls perfTuple_{DoublePhoton_FlatPt-1To100,MultiPion_PT0to200}_${PU}.${V}.root);
         python scripts/respCorrSimple.py $NTUPLES $PLOTDIR/$W -p mixmix  -w L1RawHGCal_pt -e L1RawHGCal_pt --fitrange 15 100 --root hadcorr_HGCal3D_Ref_110X.root \
                    --emf-slices L1RawHGCalEM_pt02/L1RawHGCal_pt02 0.125,0.250,0.50,0.875,1.125  --ptmax 100 --hgcal-eta && \
         cp -v hadcorr_HGCal3D_Ref_110X.root  $CMSSW_BASE/src/L1Trigger/Phase2L1ParticleFlow/data && \
         python scripts/respCorrSimple.py $NTUPLES $PLOTDIR/$W -p mixmix  -w L1HGCal3DAKT12_pt -e L1HGCal3DAKT12_pt --fitrange 15 100 --root hadcorr_HGCal3D_AKT12_110X.root \
                    --emf-slices L1HGCal3DAKT12EMRaw_pt02/L1HGCal3DAKT12_pt02 0.125,0.250,0.50,0.875,1.125  --ptmax 100 --hgcal-eta && \
         cp -v hadcorr_HGCal3D_AKT12_110X.root  $CMSSW_BASE/src/L1Trigger/Phase2L1ParticleFlow/data && \
         python scripts/respCorrSimple.py $NTUPLES $PLOTDIR/$W -p mixmix  -w L1HGCal3DS0_pt -e L1HGCal3DS0_pt --fitrange 15 100 --root hadcorr_HGCal3D_S0_110X.root \
                    --emf-slices L1HGCal3DS0EMRaw_pt02/L1HGCal3DS0_pt02 0.125,0.250,0.50,0.875,1.125  --ptmax 100 --hgcal-eta && \
         cp -v hadcorr_HGCal3D_S0_110X.root  $CMSSW_BASE/src/L1Trigger/Phase2L1ParticleFlow/data && \
         python scripts/respCorrSimple.py $NTUPLES $PLOTDIR/$W -p mixmix  -w L1HGCal3DT2_pt -e L1HGCal3DT2_pt --fitrange 15 100 --root hadcorr_HGCal3D_T2_110X.root \
                    --emf-slices L1HGCal3DT2EMRaw_pt02/L1HGCal3DT2_pt02 0.125,0.250,0.50,0.875,1.125  --ptmax 100 --hgcal-eta && \
         cp -v hadcorr_HGCal3D_T2_110X.root  $CMSSW_BASE/src/L1Trigger/Phase2L1ParticleFlow/data
         ;;
    plot-pu0)
         NTUPLES=$(ls perfTuple_{DoublePhoton_FlatPt-1To100,MultiPion_PT0to200}_PU0.${V}.root);
         WHATPLOTS="test-hgc3b" #, "test-hgc1,test-hgc2,test-hgc3,test-hgc4,test-hgc4b" 
         python scripts/respPlots.py $NTUPLES $PLOTDIR/$W/ParticleGun_PU0  -w $WHATPLOTS -p photon,pion -G --eta 1.3 3.3 --no-pt  --ymax 1.8
         python scripts/respPlots.py $NTUPLES $PLOTDIR/$W/ParticleGun_PU0  -w $WHATPLOTS -p pion        -G --eta 1.7 2.3 --no-eta --ptmax 100 --ymaxRes 1.2  --ymax 2.2
         python scripts/respPlots.py $NTUPLES $PLOTDIR/$W/ParticleGun_PU0  -w $WHATPLOTS -p photon      -G --eta 1.7 2.3 --no-eta --ptmax 100 --ymaxRes 0.3  --ymax 2.2
         ;;
    plot-pu200)
         NTUPLES=$(ls perfTuple_{SinglePion_PT0to200,DoublePhoton_FlatPt-1To100}_PU200.${V}.root);
         WHATPLOTS="test-hgc1,test-hgc3b,test-hgc4b" #3b"  1,test-hgc2,test-hgc3,test-hgc4,test-hgc4b" 
         #python scripts/respPlots.py $NTUPLES $PLOTDIR/$W/ParticleGun_PU200  -w $WHATPLOTS -p photon,pion -G --eta 1.3 3.3 --no-pt  --ymax 2.4 --ptdef ptbest
         python scripts/respPlots.py $NTUPLES $PLOTDIR/$W/ParticleGun_PU200  -w $WHATPLOTS -p pion        -G --eta 1.7 2.3 --no-eta --ptmax 100 --ymaxRes 1.6  --ymax 2.2
         #python scripts/respPlots.py $NTUPLES $PLOTDIR/$W/ParticleGun_PU200  -w $WHATPLOTS -p photon      -G --eta 1.7 2.3 --no-eta --ptmax 100 --ymaxRes 0.7  --ymax 2.2
         ;;

    plot-jets0)
         NTUPLES="perfTuple_TTbar_PU0.${V}.root"
         WHATPLOTS="test-hgc1,test-hgc2,test-hgc3,test-hgc4,test-hgc3b,test-hgc4b" 
         python scripts/respPlots.py $NTUPLES $PLOTDIR/plot-jets/TTbar_PU0 -p jet -G --eta 1.3 3.3 --no-pt   -w $WHATPLOTS 
         python scripts/respPlots.py $NTUPLES $PLOTDIR/plot-jets/TTbar_PU0 -p jet -G --eta 1.7 2.3 --no-eta  -w $WHATPLOTS 
         ;;
    plot-jets200)
         NTUPLES="perfTuple_TTbar_PU200.${V}.root"
         WHATPLOTS=test-hgc5,test-hgc5b #"test-hgc1,test-hgc2,test-hgc3,test-hgc4,test-hgc3b,test-hgc4b" 
         python scripts/respPlots.py $NTUPLES $PLOTDIR/plot-jets/TTbar_PU200 -p jet -G --eta 1.3 3.3 --no-pt  --ymax 3 -w $WHATPLOTS 
         python scripts/respPlots.py $NTUPLES $PLOTDIR/plot-jets/TTbar_PU200 -p jet -G --eta 1.7 2.3 --no-eta --ymax 3 -w $WHATPLOTS 
         ;;
     plots-pf)
         if [[ "$PU" == "PU0" ]]; then
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p electron,photon  -g  --ymaxRes 0.35 --ptmax 100 -E 3.0
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p pion,mixmix      -g  --ymaxRes 1.2  --ptmax 100 -E 3.0
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p kshort           -g  --ymaxRes 1.2  --ptmax 100 --eta 1.3 3.3 --ptdef pt02,pt
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p pion,photon,mixmix -g  --eta 3.0 5.0  --ymax 3 --ymaxRes 1.5 --label hf  --no-fit 
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p pion,photon,mixmix -g  --eta 3.5 4.5  --ymax 3 --ymaxRes 1.5 --label hf  --no-fit --no-eta
         else
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p electron,photon,pizero -g  --ymax 2.5 --ymaxRes 0.6 --ptmax 80 -E 3.0
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p pion,klong,mixmix       -g  --ymax 2.5 --ymaxRes 1.5 --ptmax 80 -E 3.0
             python scripts/respPlots.py $NTUPLES $PLOTDIR/ParticleGun_${PU} -w l1pf -p pion,pizero,mixmix      -g  --ymax 3.0 --ymaxRes 1.5 --ptmax 80 --eta 3.0 5.0 --label hf  --no-fit 
         fi;
         ;;

esac;
