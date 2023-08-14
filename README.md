# Project Using the W5100S-EVB-PICO Board

## Overview


In this project, we are using two W5100S-EVB-PICO boards.

1. The first board connects an Arducam and Ethernet to serve the role of transmitting a picture to a web page upon receiving a web request.
2. The second board uses the Replicate API over the network to obtain the web address of the photo transmitted by the first PICO board. It then captions this image and sends the result back to the PICO board. The PICO board then displays this response on an ssd1306 oled screen.

## Models Used

- [Model testable on Replicate](https://replicate.com/andreasjansson/blip-2)
- [Research paper on the model](https://arxiv.org/abs/2301.12597)
- [Official GitHub](https://github.com/salesforce/LAVIS/tree/main/projects/blip2)

## Potential Developments

The current focus of this project is on captioning an image and displaying the text. However, by adding speakers in the future, this could evolve into applications for the visually impaired or anomaly detection, among various other project ideas.
