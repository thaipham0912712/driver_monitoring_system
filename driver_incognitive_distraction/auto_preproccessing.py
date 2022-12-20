import argparse
import preprocessing
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
            blink_video.blink_detector(os.path.join(root,output_name), os.path.join(root,file))

def arg_parse():
    parser = argparse.ArgumentParser(description='Blinks detector auto script')
    parser.add_argument('--data_dir', '-d', type=str, required=True,
                        help='Path to data dir')

    args = parser.parse_args()
    return args

if __name__=="__main__":
    args = arg_parse()
    main(args.data_dir)
    # path1 is the address to the folder of all subjects, each subject has three txt files for alert, semisleepy and sleepy levels
    path1 = 'Drowsiness Data'
    window_size = 30
    stride = 2
    Training = './Blinks_30_Fold3.npy'
    Testing = './BlinksTest_30_Fold3.npy'
    # Normalizing with respect to different individuals####First Phase
    blinks, labels, blinksTest, labelTest = Preprocess(
        path1, window_size, stride, test_fold='Fold3')
    # np.save(open(Training,'wb'),blinks)
    # np.save(open('./Labels_30_Fold3.npy', 'wb'),labels)
    np.save(open(Testing, 'wb'), blinksTest)
    np.save(open('./LabelsTest_30_Fold3.npy', 'wb'), labelTest)
