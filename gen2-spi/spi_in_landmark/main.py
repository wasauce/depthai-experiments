import cv2
import numpy as np
import depthai as dai
from time import sleep

'''
This a hello world for the SPIIn node. It basically just returns whatever is sent in right back out.
'''

# Any data that's passed in will be passed back out the SPI interface.
def create_spi_demo_pipeline():
    print("Creating SPI pipeline: ")
    print("COLOR CAM -> ENCODER -> SPI OUT")
    pipeline = dai.Pipeline()

    nn1 = pipeline.createNeuralNetwork()
    spiout_meta = pipeline.createSPIOut()
    spiin_nn = pipeline.createSPIIn()

    spiin_nn.setStreamName("spiin")
    spiin_nn.setBusId(0)


    nn1.setBlobPath("landmarks-regression-retail-0009.blob")
    spiin_nn.out.link(nn1.input)


    spiout_meta.setStreamName("spimeta")
    spiout_meta.setBusId(0)

#    spiin_nn.out.link(spiout_meta.input)
    nn1.out.link(spiout_meta.input)

    return pipeline


def test_pipeline():
    pipeline = create_spi_demo_pipeline()

    print("Creating DepthAI device")
    if 1:
        device = dai.Device(pipeline)
    else: # For debug mode, with the firmware already loaded
        found, device_info = dai.XLinkConnection.getFirstDevice(
                dai.XLinkDeviceState.X_LINK_UNBOOTED)
        if found:
            device = dai.Device(pipeline, device_info)
        else:
            raise RuntimeError("Device not found")
    print("Starting pipeline")
    device.startPipeline()

    print("Pipeline is running. See connected SPI device for output!")

    while True:
        sleep(1)

    print("Closing device")
    del device

test_pipeline()
