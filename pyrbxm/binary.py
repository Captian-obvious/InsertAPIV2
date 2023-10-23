from __future__ import annotations
import lz4.block
import struct
from io import BytesIO
from dataclasses import dataclass
import numpy as np

from .tree import PropertyType, Instance

# https://blog.roblox.com/2013/05/condense-and-compress-our-custom-binary-file-format/
def decode_int(i):
    return (i >> 1) ^ (-(i & 1))
##end
def encode_int(i):
    return (i << 1) ^ (i >> 31)
##end
# http://stackoverflow.com/questions/442188/readint-readbyte-readstring-etc-in-python
class BinaryStream:
    UINT32 = np.dtype(">i4")
    F32 = np.dtype(">f4")
    def __init__(self, base_stream):
        self.base_stream = base_stream
    ##end
    def read_bytes(self, length) -> bytes:
        return self.base_stream.read(length)
    ##end
    def write_bytes(self, value):
        self.base_stream.write(value)
    ##end
    def unpack(self, fmt):
        return struct.unpack(fmt, self.read_bytes(struct.calcsize(fmt)))
    ##end
    def pack(self, fmt, *data):
        return self.write_bytes(struct.pack(fmt, *data))
    ##end
    def read_string(self):
        (length,) = self.unpack("<I")
        return self.read_bytes(length).decode("utf8")
    ##end
    def write_string(self, s):
        self.pack("<I", len(s))
        self.write_bytes(s.encode("utf8"))
    ##end
    # https://blog.roblox.com/2013/05/condense-and-compress-our-custom-binary-file-format/
    def read_interleaved(self, count: int, size: int = 4):
        return (
            np.frombuffer(self.read_bytes(count * size), np.uint8)
            .reshape(size, count)
            .T.flatten()
        )
    ##end
    def read_ints(self, count):
        return decode_int(self.read_interleaved(count).view(self.UINT32))
    ##end
    def write_ints(self, values):
        self.pack(f"<{len(values)}f", *values)
    ##end
    def read_floats(self, count):
        return self.read_ints(count).view(self.F32)
    ##end
    def write_floats(self, values):
        self.pack(f"<{len(values)}f", *values)
    ##end
    def read_instance_ids(self, count):
        """Reads and accumulates an interleaved buffer of integers."""
        return self.read_ints(count).cumsum()
    ##end
    def write_instance_ids(self, values):
        """Accumulatively writes an interleaved array of integers."""
        self.write_ints(np.ediff1d(np.asarray(values), to_begin=values[0]))
    ##end
    # http://stackoverflow.com/questions/32774910/clean-way-to-read-a-null-terminated-c-style-string-from-a-file
    def readCString(self):
        buf = bytearray()
        while True:
            b = self.base_stream.read(1)
            if b is None or b == b"\0":
                return buf
            else:
                buf.extend(b)
            ##endif
        ##end
    ##end
    def writeCString(self, string):
        self.write_bytes(string)
        self.write_bytes(b"\0")
    ##end
class META:
    def __init__(self):
        self.Data = {}
    ##end
    def deserialize(self, stream: BinaryStream, file):
        (numEntries,) = stream.unpack("<i")
        for i in range(numEntries):
            key = stream.read_string()
            value = stream.read_string()
            self.Data[key] = value
        ##end
        file.META = self
    ##end
    def serialize(self, stream: BinaryStream):
        stream.pack("<i", len(self.Data))
        for key, value in self.Data.items():
            stream.write_string(key)
            stream.write_string(value)
        ##end
    ##end
    def dump(self):
        print(f"- NumEntries: {len(self.Data)}")
        for key, value in self.Data.items():
            print(f"  - {key}: {value}")
        ##end
    ##end
##end
class INST:
    def __init__(self):
        self.ClassIndex = 0
        self.ClassName = ""
        self.IsService = False
        self.RootedServices = []
        self.NumInstances = 0
        self.InstanceIds = []
    ##end
    def __str__(self):
        return f"{self.ClassIndex}: {self.ClassName}x{self.NumInstances}"
    ##end
    def deserialize(self, stream: BinaryStream, file: BinaryRobloxFile):
        (self.ClassIndex,) = stream.unpack("<i")
        self.ClassName = stream.read_string()
        self.IsService, self.NumInstances = stream.unpack("<bi")
        self.InstanceIds = stream.read_instance_ids(self.NumInstances)
        file.Classes[self.ClassIndex] = self
        if self.IsService:
            self.RootedServices = []
            for i in range(self.NumInstances):
                isRooted = stream.unpack("<b")
                self.RootedServices.append(isRooted)
            ##end
        ##endif
        for i in range(self.NumInstances):
            instId = self.InstanceIds[i]
            # inst = Activator.CreateInstance(instType) as Instance;
            inst = Instance(self.ClassName)
            inst.Referent = str(instId)
            inst.IsService = self.IsService
            if self.IsService:
                isRooted = self.RootedServices[i]
                inst.Parent = file if isRooted else None
            ##endif
            file.Instances[instId] = inst
        ##end
        def serialize(self, stream: BinaryStream, file: BinaryRobloxFile):
            stream.pack("<i", self.ClassIndex)
            stream.write_string(self.ClassName)
            stream.pack("<bi", self.IsService, self.NumInstances)
            stream.write_instance_ids(self.InstanceIds)
            if self.IsService:
                for instId in self.InstanceIds:
                    # Instance service = file.Instances[instId];
                    # writer.Write(service.Parent == file);
                    stream.pack("<b", False)
                ##end
            ##endif
        ##end
        def dump(self):
            print(f"- ClassIndex:   {self.ClassIndex}")
            print(f"- ClassName:    {self.ClassName}")
            print(f"- IsService:    {self.IsService}")
            if self.IsService and self.RootedServices is not None:
                print(f"- RootedServices: `{', '.join(self.RootedServices)}`")
            ##endif
            print(f"- NumInstances: {self.NumInstances}")
            print(f"- InstanceIds: `{', '.join(self.InstanceIds)}`")
        ##end
    ##end
##end
@dataclass
class PROP:
    File: BinaryRobloxFile = None
    Name: str = ""
    ClassIndex: int = -1
    Type: PropertyType = PropertyType.Unknown
    @property
    def Class(self):
        return self.File.Classes[self.ClassIndex]
    ##end
    @property
    def ClassName(self):
        return self.Class.ClassName if self.Class else "UnknownClass"
    ##end
    def __str__(self):
        return f"{self.Type} {self.ClassName}.{self.Name}"
    ##end
    def deserialize(self, stream: BinaryStream, file: RobloxBinaryFile):
        self.File = file
        (self.ClassIndex,) = stream.unpack("<i")
        self.Name = stream.read_string()
        (propType,) = stream.unpack("<b")
        self.Type = PropertyType(propType)
        assert (
            self.Class is not None
        ), f"Unknown class index {self.ClassIndex} (@ {self})!"
        ids = self.Class.InstanceIds
        instCount = self.Class.NumInstances
    ##end
##end


class BinaryRobloxFileChunk:
    """
    BinaryRobloxFileChunk represents a generic LZ4 - compressed chunk
    of data in Roblox's Binary File Format.
    """

    def __init__(self):
        self.ChunkType = b""
        self.Reserved = -1
        self.CompressedSize = -1
        self.Size = -1
        self.CompressedData = b""
        self.Data = b""
        self.HasWriteBuffer = False
        self.WriteBuffer = bytearray()
        self.Handler = None
    ##end
    @property
    def HasCompressedData(self):
        return self.CompressedSize > 0
    ##end
    def __str__(self):
        chunkType = self.ChunkType.replace(b"\0", b" ")
        return f"'{chunkType}' Chunk ({self.Size} bytes) [{self.Handler}]"
    ##end
    def deserialize(self, stream: BinaryStream):
        (
            self.ChunkType,
            self.CompressedSize,
            self.Size,
            self.Reserved,
        ) = stream.unpack("<4siii")

        if self.HasCompressedData:
            self.CompressedData = stream.read_bytes(self.CompressedSize)
            self.Data = lz4.block.decompress(self.CompressedData, self.Size)
            # print(self.Data)
        else:
            self.Data = stream.read_bytes(self.Size)
        ##endif
    ##end
##end


class BinaryRobloxFile(Instance):  # (RobloxFile):
    # Header Specific
    MAGIC_HEADER = b"<roblox!\x89\xff\x0d\x0a\x1a\x0a"

    def __init__(self):
        # Header Specific
        self.Version = 0
        self.NumClasses = 0
        self.NumInstances = 0
        self.Reserved = 0

        # Runtime Specific
        self.ChunksImpl: list[BinaryRobloxFileChunk] = []

        self.Instances = []
        self.Classes = []

        self.META = None
        self.SSTR = None
        self.SIGN = None

        self.Name = "Bin:"
        self.Referent = "-1"
        self.ParentLocked = True
    ##end
    @property
    def Chunks(self):
        return self.ChunksImpl
    ##end
    @property
    def HasMetadata(self):
        return self.META is not None
    ##end
    @property
    def Metadata(self):
        return self.META.Data if self.META else {}
    ##end
    @property
    def HasSharedStrings(self):
        return self.SSTR is not None
    ##end
    @property
    def SharedStrings(self):
        return self.SSTR.Strings if self.SSTR else {}
    ##end
    @property
    def HasSignatures(self):
        return self.SIGN is not None
    ##end
    @property
    def Signatures(self):
        return self.SIGN.Signatures if self.SIGN else []
    ##end
    def deserialize(self, file):
        stream = BinaryStream(file)
        # Verify the signature of the file.
        signature = stream.read_bytes(14)
        if signature != self.MAGIC_HEADER:
            raise ValueError(
                "Provided file's signature does not match BinaryRobloxFile.MAGIC_HEADER!"
            )
        ##endif
        # Read header data.
        (
            self.Version,
            self.NumClasses,
            self.NumInstances,
            self.Reserved,
        ) = stream.unpack("<HIIq")
        # Begin reading the file chunks.
        reading = True
        self.Classes = [None] * self.NumClasses
        self.Instances = [None] * self.NumInstances
        while reading:
            chunk = BinaryRobloxFileChunk()
            chunk.deserialize(stream)
            handler = None
            if chunk.ChunkType == b"INST":
                handler = INST()
            elif chunk.ChunkType == b"PROP":
                handler = PROP()
            elif chunk.ChunkType == b"PRNT":
                handler = None  # PRNT();
            elif chunk.ChunkType == b"META":
                handler = META()
            elif chunk.ChunkType == b"SSTR":
                handler = None  # SSTR();
            elif chunk.ChunkType == b"SIGN":
                handler = None  # SIGN();
            elif chunk.ChunkType == b"END\0":
                reading = False
            else:
                self.LogError(
                    f"BinaryRobloxFile - Unhandled chunk-type: {chunk.ChunkType}!"
                )
            ##endif
            if handler:
                chunk_stream = BinaryStream(BytesIO(chunk.Data))
                chunk.Handler = handler
                handler.deserialize(chunk_stream, self)
            ##endif
            self.ChunksImpl.append(chunk)
        ##end
    ##end
##end
