#!/usr/bin/env python3

from Gaugi      import LoggingLevel, Logger
from Gaugi                import GeV
from CaloCell.CaloDefs    import CaloSampling
from G4Kernel.utilities   import *
import numpy as np
import argparse
import sys,os


mainLogger = Logger.getModuleLogger("job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-i','--inputFile', action='store', dest='inputFile', required = True,
                    help = "The event input file generated by the Pythia event generator.")

parser.add_argument('-p','--pileupFile', action='store', dest='pileupFile', required = True,
                    help = "The event HIT file to be merged (pileup)")

parser.add_argument('-o','--outputFile', action='store', dest='outputFile', required = True,
                    help = "The reconstructed event file generated by lzt/geant4 framework.")

parser.add_argument('-d', '--debug', action='store_true', dest='debug', required = False,
                    help = "In debug mode.")

parser.add_argument('--evt','--numberOfEvents', action='store', dest='numberOfEvents', required = False, type=int, default=-1,
                    help = "The number of events to apply the reconstruction.")

parser.add_argument('--outputLevel', action='store', dest='outputLevel', required = False, type=int, default=3,
                    help = "The output level messenger.")


pi = np.pi

if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


outputLevel = 0 if args.debug else args.outputLevel

try:

  
  from GaugiKernel import ComponentAccumulator
  acc = ComponentAccumulator("ComponentAccumulator", args.outputFile)


  # the reader must be first in sequence
  from RootStreamBuilder import RootStreamHITReader
  reader = RootStreamHITReader("HITReader", 
                                InputFile       = args.inputFile,
                                HitsKey         = recordable("Hits"),
                                EventKey        = recordable("EventInfo"),
                                TruthKey        = recordable("Particles"),
                                NtupleName      = "CollectionTree",
                              )
  reader.merge(acc)



  from PileupMergeBuilder import PileupMerge
  pileup = PileupMerge( "PileupMerge", 
                        InputFile       = args.pileupFile,
                        InputHitsKey    = recordable("Hits"),
                        InputEventKey   = recordable("EventInfo"),
                        OutputHitsKey   = recordable("Hits") + "_Merged",
                        OutputEventKey  = recordable("EventInfo") + "_Merged",
                        NtupleName      = "CollectionTree",
                        OutputLevel     = outputLevel
                      )
  acc += pileup




  from RootStreamBuilder import RootStreamHITMaker
  HIT = RootStreamHITMaker( "RootStreamHITMaker",
                             # input from context
                             InputHitsKey    = recordable("Hits")+"_Merged",
                             InputEventKey   = recordable("EventInfo")+"_Merged",
                             InputTruthKey   = recordable("Particles"),
                             # output to file
                             OutputHitsKey   = recordable("Hits"),
                             OutputEventKey  = recordable("EventInfo"),
                             OutputTruthKey  = recordable("Particles"),
                             OutputLevel     = outputLevel)
  acc += HIT
  acc.run(args.numberOfEvents)
  sys.exit(0)
  
except  Exception as e:
  print(e)
  sys.exit(1)
