import os
import abc


class DatabaseInterface(object):
    def __init__(self, *args, **kwargs):
        self.dbtype = None
        self.path = os.path.join(os.getcwd(), args[0])
        self.records = []
        self.count = 1
        self.header = None
        self.items = None  # for current line
        self.kernel_extracted = kwargs.pop('kernel_extracted', False)
        self.brand = kwargs.pop('brand', None)

    @abc.abstractmethod
    def parse_pre(self, line, **kwargs):
        pass

    def get_firmware(self, *args, **kwargs):
        with open(self.path) as f:
            for line in f:
                context = self.parse_pre(line.strip())
                if context is None:
                    continue
                context['id'] = self.count
                yield context
                self.count += 1

    def get_count(self, *args, **kwargs):
        return self.count


class DatabaseFirmadyne(DatabaseInterface):
    def parse_pre(self, line, **kwargs):
        items = line.split(',')
        if len(items) != 11:
            return
        if self.header is None:
            self.header = items
            return
        kernel_extracted = items[self.header.index('kernel_extracted')]
        if self.kernel_extracted and kernel_extracted != 't':
            return
        path = items[self.header.index('filename')]
        uuid = items[self.header.index('id')]
        brand = items[self.header.index('brand')]
        if self.brand is not None and brand != self.brand:
            return
        if not len(items[self.header.index('arch')]):
            arch = None
            endian = None
        else:
            arch = items[self.header.index('arch')][:-2]
            endian = items[self.header.index('arch')][-1:]
        kernel_version = items[self.header.index('kernel_version')]
        description = items[self.header.index('description')]
        url = items[self.header.index('url')]
        self.items = {
            'uuid': uuid, 'path': path, 'brand': brand, 'arch': arch, 'kernel_version': kernel_version,
            'endian': endian, 'description': description, 'url': url, 'kernel_extracted': kernel_extracted == 't'
        }
        return self.items

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbtype = 'firmadyne'


class DatabaseText(DatabaseInterface):
    def parse_pre(self, line, **kwargs):
        items = line.split()
        if self.header is None:
            self.header = items
            return
        path = items[self.header.index('path')]
        uuid = items[self.header.index('uuid')]
        arch = items[self.header.index('arch')]
        endian = items[self.header.index('endian')]
        brand = items[self.header.index('brand')]
        self.items = {'uuid': uuid, 'path': path, 'brand': brand, 'arch': arch, 'endian': endian}
        return self.items

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbtype = 'text'

