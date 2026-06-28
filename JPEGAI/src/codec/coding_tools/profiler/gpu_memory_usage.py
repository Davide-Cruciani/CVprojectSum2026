# The copyright in this software is being made available under the BSD
# License, included below. This software may be subject to other third party
# and contributor rights, including patent rights, and no such rights are
# granted under this license.
#
# Copyright (c) 2010-2022, ITU/ISO/IEC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * Neither the name of the ITU/ISO/IEC nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

import os
from datetime import datetime
import pandas as pd

import pynvml

pynvml.nvmlInit()


def _gpu_mem():
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return info.total // 1024**2, info.used // 1024**2


class GpuMemoryUsage:
    def __init__(self):
        total, used = _gpu_mem()

        self.table = pd.DataFrame({
            '_START_': datetime.now(),
            'Event': 'Initialization',
            'Total, MB': total,
            'Start GPU memory usage, MB': used,
            'Finish GPU memory usage, MB': '',
            'Difference, MB': ''
        }, index=[0])

        self.directory = ''
        self.buffer = dict()

    def set_directory(self, path):
        os.makedirs(os.path.join(path, 'GPU_MEMORY_USAGE'), exist_ok=True)
        self.directory = os.path.join(path, 'GPU_MEMORY_USAGE')

    def add_event(self, event):
        total, used = _gpu_mem()

        self.buffer[event] = {
            '_START_': datetime.now(),
            'Event': event,
            'Total, MB': total,
            'Start GPU memory usage, MB': used,
            'Finish GPU memory usage, MB': '',
            'Difference, MB': ''
        }

        self.table = pd.concat([self.table, pd.DataFrame([self.buffer[event]])], ignore_index=True)

    def start(self, event):
        total, used = _gpu_mem()
        self.buffer[event] = {
            '_START_': datetime.now(),
            'Event': event,
            'Total, MB': total,
            'Start GPU memory usage, MB': used
        }

    def finish(self, event):
        used = _gpu_mem()[1]
        self.buffer[event]['Finish GPU memory usage, MB'] = used
        self.buffer[event]['Difference, MB'] = (
            self.buffer[event]['Finish GPU memory usage, MB']
            - self.buffer[event]['Start GPU memory usage, MB']
        )

        self.table = pd.concat([self.table, pd.DataFrame([self.buffer[event]])], ignore_index=True)

    def save_results(self, filename='GPU_MEMORY_USAGE'):
        output_name = filename + '.CSV'

        df = self.table.sort_values(by='_START_').drop(columns=['_START_'])

        if self.directory:
            df.to_csv(os.path.join(self.directory, output_name), index=False)
        else:
            df.to_csv(output_name, index=False)