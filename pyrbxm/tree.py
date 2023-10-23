from enum import Enum
from .datatypes import UniqueId


# fmt: off
class PropertyType(Enum):
    Unknown            =  0
    String             =  1
    Bool               =  2
    Int                =  3
    Float              =  4
    Double             =  5
    UDim               =  6
    UDim2              =  7
    Ray                =  8
    Faces              =  9
    Axes               = 10
    BrickColor         = 11
    Color3             = 12
    Vector2            = 13
    Vector3            = 14

    CFrame             = 16
    Quaternion         = 17
    Enum               = 18
    Ref                = 19
    Vector3int16       = 20
    NumberSequence     = 21
    ColorSequence      = 22
    NumberRange        = 23
    Rect               = 24
    PhysicalProperties = 25
    Color3uint8        = 26
    Int64              = 27
    SharedString       = 28
    ProtectedString    = 29
    OptionalCFrame     = 30
    UniqueId           = 31
    FontFace           = 32
##end
# fmt: on


class Instance:
    """
    Describes an object in Roblox's DataModel hierarchy.
    Instances can have sets of properties loaded from *.rbxl/*.rbxm files.
    """

    def __init__(self, ClassName):

        """A list of properties that are defined under this Instance."""
        self.props = {}
        """ The raw list of children for this Instance. """
        self.Children: set[Instance] = set()
        """ The raw unsafe value of the Instance's parent. """
        self.ParentUnsafe: Instance = None
        """The ClassName of this Instance."""
        self.ClassName: str = ClassName
        """ The name of this Instance. """
        self.Name: str = self.ClassName
        """ Indicates whether this Instance should be serialized. """
        self.Archivable: bool = True
        """ The source AssetId this instance was created in. """
        self.SourceAssetId: int = -1
        """ A unique identifier declared for this instance. """
        self.UniqueId: UniqueId = None
        """ A context-dependent unique identifier for this instance when being serialized. """
        self.Referent: str = None
        """ Indicates whether the parent of this object is locked. """
        self.ParentLocked: bool = False
        """ Indicates whether this Instance is a Service. """
        self.IsService: bool = False
        """ Indicates whether this Instance has been destroyed. """
        self.Destroyed: bool = False
        """ A hashset of CollectionService tags assigned to this Instance. """
        self.Tags: set[str] = set()
        """ The public readonly access point of the attributes on this Instance. """
        # self.Attributes: RbxAttributes = RbxAttributes()
        # self.RefreshProperties()
    ##end
    # @property
    # def ClassName(self):
    #     """The ClassName of this Instance."""
    #     return self.GetType().Name

    def __str__(self):
        """The name of this Instance, if a Name property is defined."""
        return self.Name
    ##end
    @property
    def AttributesSerialize(self) -> bytes:
        """The internal serialized data of this Instance's attributes"""
        return self.Attributes.Save()
    ##end
    @AttributesSerialize.setter
    def AttributesSerialize(self, value: bytes):
        self.Attributes.Load(value)
    ##end
    @property
    def SerializedTags(self) -> bytes:
        """
        Internal format of the Instance's CollectionService tags.
        Property objects will look to this member for serializing the Tags property.
        """
        if not self.Tags:
            return None
        ##endif
        return "\0".join(self.Tags).encode()
    ##end
    @SerializedTags.setter
    def SerializedTags(self, value: bytes):
        """
        Internal format of the Instance's CollectionService tags.
        Property objects will look to this member for serializing the Tags property.
        """
        buffer = bytearray()
        self.Tags.clear()
        for i, id in enumerate(value):
            if id != 0:
                buffer.append(id)
            ##endif
            if id == 0 or i == (len(value) - 1):
                self.Tags.append(buffer.decode())
                buffer.clear()
            ##endif
        ##endif
    ##end
##end
