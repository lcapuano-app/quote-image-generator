import sys
import getopt

"""
  argv -> list[str]

  Sets the default values to env, type and riot id ( check config.py for details) then checks if it recieves any
  changes to this values from the comand line exec (sys.argv as param)

"""
def get_params( argv ):
  arg_quote = '63139372217ba7e20813b932'
  arg_output = 'output'
  arg_help = "{0} \r\n -q <quoteId> => Database quote ID\r\n -o <outtput> => file output path".format(argv[0])

  try:
    opts, args = getopt.getopt(argv[1:], "hq:o:", ["help", "quote=", "output="])
  except:
    print(arg_help)
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print(arg_help)  # print the help message
      sys.exit(3)
    elif opt in ("-q", "--quote"):
      arg_quote = arg
    elif opt in ("-o", "--output"):
      arg_output = arg


  return arg_quote, arg_output
