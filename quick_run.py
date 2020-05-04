"""
MIT License

Copyright (c) 2019 Sadeep Jayasumana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse

import torch

from crfasrnn import util
from crfasrnn.crfasrnn_model import CrfRnnNet


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--weights",
        help="Path to the .pth file (download from https://tinyurl.com/crfasrnn-weights-pth)",
        required=True,
    )
    parser.add_argument("--image", help="Path to the input image", required=True)
    parser.add_argument("--output", help="Path to the output label image", default=None)
    args = parser.parse_args()

    img_data, img_h, img_w, size = util.get_preprocessed_image(args.image)

    output_file = args.output or args.image + "_labels.png"

    model = CrfRnnNet()
    model.load_state_dict(torch.load(args.weights))
    model.eval()
    out = model.forward(torch.from_numpy(img_data))

    probs = out.detach().numpy()[0]
    label_im = util.get_label_image(probs, img_h, img_w, size)
    label_im.save(output_file)


if __name__ == "__main__":
    main()
