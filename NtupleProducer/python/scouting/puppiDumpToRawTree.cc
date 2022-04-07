#include <cstdio>
#include <cstdint>
#include <fstream>
#include <string>
#include <TTree.h>
#include <TFile.h>
#include <Compression.h>
#include <TROOT.h>
#include <TStopwatch.h>

int main(int argc, char**argv) {
    uint64_t header, data[255];
    uint16_t run, bx;
    uint32_t orbit;
    UInt_t npuppi; // issues with uint8_t that root sees to max at 127

    int iarg = 1, narg = argc - 1;
    if (std::string(argv[iarg]) == "-j") {
        ROOT::EnableImplicitMT(std::stoi(argv[iarg+1])); 
        printf("Enabled Implicit MT with %d threads\n", std::stoi(argv[iarg+1]));
        iarg += 2; narg -= 2;
    }
    std::fstream fin(argv[iarg], std::ios_base::in | std::ios_base::binary);

    int compressionAlgo, compressionLevel = 0;
    if (narg >= 4) {
        std::string compressionName(argv[iarg+2]);
        if (compressionName == "lzma") compressionAlgo = ROOT::RCompressionSetting::EAlgorithm::kLZMA;
        else if (compressionName == "zlib") compressionAlgo = ROOT::RCompressionSetting::EAlgorithm::kZLIB;
        else if (compressionName == "lz4") compressionAlgo = ROOT::RCompressionSetting::EAlgorithm::kLZ4;
        else if (compressionName == "zstd") compressionAlgo = ROOT::RCompressionSetting::EAlgorithm::kZSTD;
        else {
            printf("Unsupported compression algo %s\n", argv[iarg+2]);
            return 1;
        }
        compressionLevel = std::stoi(argv[iarg+3]);
    }
    TFile *fout = TFile::Open(argv[iarg+1], "RECREATE", "", compressionLevel);
    if (compressionLevel) fout->SetCompressionAlgorithm(compressionAlgo);
    TTree *tree = new TTree("Events","Events");
    tree->Branch("run", &run, "run/s");
    tree->Branch("orbit", &orbit, "orbit/i");
    tree->Branch("bx", &bx, "bx/s");
    tree->Branch("nPuppi", &npuppi, "nPuppi/i");
    tree->Branch("Puppi_w64", &data, "Puppi_w64[nPuppi]/l");

    TStopwatch timer; timer.Start();
    unsigned long entries = 0;
    while(fin.good()) {
        fin.read(reinterpret_cast<char*>(&header), sizeof(uint64_t));
        npuppi = header          & 0xFFF;
        bx     = (header >> 12)  & 0xFFF;
        orbit  = (header >> 24)  & 0X3FFFFFFF;
        run    = (header >> 54);
        if (npuppi) {
            fin.read(reinterpret_cast<char*>(&data[0]), npuppi*sizeof(uint64_t));
        }
        tree->Fill();
        if ((++entries) % 100000 == 0) {
            printf("Processed %8lu entries\n",entries);
        }
    }
    tree->Write();
    fout->Close();
    timer.Stop();
    double tcpu = timer.CpuTime(), treal = timer.RealTime();
    printf("Done in %.2fs (cpu), %.2fs (real). Event rate: %.1f kHz\n", tcpu, treal, entries/treal/1000.);
    return 0;
}
