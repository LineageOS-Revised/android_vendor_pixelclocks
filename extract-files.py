#!/usr/bin/env -S PYTHONPATH=../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
import sys
from os import path

from extract_utils.extract_pixel import (
    extract_pixel_factory_image,
    pixel_factory_image_regex,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.tools import android_root
from extract_utils.utils import remove_dir_contents

DEFAULT_SOURCE = path.join(
    android_root,
    'pixel',
    'rango-cp2a.260605.012-factory-b6d754ad.zip',
)

extract_fns = {
    pixel_factory_image_regex: extract_pixel_factory_image,
}

class PixelClocksModule(ExtractUtilsModule):
    def cleanup(self):
        for proprietary_file in self.proprietary_files:
            vendor_path = self.proprietary_file_vendor_path(proprietary_file)
            if path.isdir(vendor_path):
                remove_dir_contents(vendor_path)
            os.makedirs(vendor_path, exist_ok=True)

        if self.rro_packages:
            os.makedirs(self.vendor_rro_path, exist_ok=True)


module = PixelClocksModule(
    'pixelclocks',
    'pixelclocks',
    device_rel_path='vendor/pixelclocks',
    extract_fns=extract_fns,
)

module.vendor_rel_path = 'vendor/pixelclocks'
module.vendor_path = path.join(android_root, module.vendor_rel_path)
module.vendor_rro_path = path.join(module.vendor_path, 'rro_overlays')

if __name__ == '__main__':
    if DEFAULT_SOURCE not in sys.argv and path.isfile(DEFAULT_SOURCE):
        sys.argv += ['--kang', DEFAULT_SOURCE]

    utils = ExtractUtils.device(module)
    utils.run()
