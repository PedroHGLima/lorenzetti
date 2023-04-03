
OUT_NAME="Zee_boosted_large"

mkdir $OUT_NAME
cd $OUT_NAME
OUT_PATH=$PWD

mkdir -p $OUT_PATH/HIT
mkdir -p $OUT_PATH/ESD
mkdir -p $OUT_PATH/EVT
mkdir -p $OUT_PATH/AOD

# generate 10k Zee events with pythia
#cd $OUT_PATH/EVT
prun_events.py -c "gen_zee_boosted.py --pileupAvg 40" -mt 40 --nov 1000000 -o Zee_boosted.EVT.root -m


# generate hits around the truth particle seed
cd ../HIT
simu_trf.py -i ../EVT/Zee_boosted.EVT.root -o Zee_boosted.HIT.root -nt 40 


# digitalization
cd ../ESD
prun_jobs.py -c "digit_trf.py" -i ../HIT/ -o Zee_boosted.ESD.root -mt 40


# reconstruction
cd ../AOD
prun_jobs.py -c "reco_trf.py" -i ../ESD -o Zee_boosted.AOD.root -mt 40 -m


cd ../..

