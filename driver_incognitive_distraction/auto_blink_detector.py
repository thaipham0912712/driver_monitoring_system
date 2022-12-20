import argparse
import blink_detector
import os
import re

def main(path):
  videolist = []
  for root, dirs, files in os.walk(path):
    for file in files:
      if(file.endswith(".mp4") or file.endswith(".mov") or file.endswith(".MOV")):
        output_name = ''
        # videolist.append(os.path.join(root,file))
        print(f"root: {root}, dirs {dirs}, file {file}")
        if bool(re.search(r"^0.[mov|MOV|mp4]", file)):
          output_name = 'alert.txt'
        elif bool(re.search(r"^5.[mov|MOV|mp4]", file)):
          output_name = 'semisleepy.txt'
        else:
          output_name = 'sleepy.txt'
        blink_detector.blink_detector(os.path.join(root,output_name), os.path.join(root,file))

def arg_parse():
  parser = argparse.ArgumentParser(description='Blinks detector auto script')
  parser.add_argument('--data_dir', '-d', type=str, required=True,
                      help='Path to data dir')

  args = parser.parse_args()
  return args

if __name__=="__main__":
  args = arg_parse()
  main(args.data_dir)