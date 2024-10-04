from argparse import ArgumentParser

def get_create_dataset_args():
    parser = ArgumentParser()
    parser.add_argument('--dataset_folder', type=str, default='./dataset')
    parser.add_argument('--font_folder', type=str, default='./fonts')
    parser.add_argument('--source_font', type=str, default='KAIU.TTF')
    parser.add_argument('--image_size', type=int, default=128)
    parser.add_argument('--font_size', type=int, default=100)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    import json

    args = get_create_dataset_args()
    print(json.dumps(args.__dict__, indent=4))
