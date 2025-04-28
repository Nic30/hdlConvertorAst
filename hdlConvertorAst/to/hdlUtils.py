from typing import Optional

from hdlConvertorAst.hdlAst._expr import HdlValueInt


class Indent(object):
    """
    indentation context
    """

    def __init__(self, autoIndentStream):
        self.s = autoIndentStream
        self.original_indent = None

    def __enter__(self):
        s = self.s
        self.original_indent = s.indent_str
        s.indent_cnt += 1
        s.indent_str = s.indent_str + s.INDENT_STEP

    def __exit__(self, exception_type, exception_value, traceback):
        s = self.s
        s.indent_cnt -= 1
        s.indent_str = self.original_indent


class UnIndent():
    """
    unindentation context
    """

    def __init__(self, autoIndentStream):
        self.s = autoIndentStream
        self.original_indent = None

    def __enter__(self):
        s = self.s
        self.original_indent = s.indent_str
        assert s.indent_cnt > 0
        s.indent_cnt -= 1
        s.indent_str = s.indent_str[0:len(s.indent_str) - len(s.INDENT_STEP)]

    def __exit__(self, exception_type, exception_value, traceback):
        s = self.s
        s.indent_cnt += 1
        s.indent_str = self.original_indent


class AutoIndentingStream():

    def __init__(self, stream, indent_step):
        """
        :param stream: output stream
        :param indent_step: string of indent
        """

        self.INDENT_STEP = indent_step
        self.stream = stream
        self.requires_indent = True
        self.indent_cnt = 0
        self.indent_str = ""

    def write(self, s):
        w = self.stream.write
        if self.requires_indent and s != "\n":
            w(self.indent_str)
        w(s)
        self.requires_indent = s.endswith("\n")

    def close(self):
        self.stream.close()


def iter_with_last(it):
    # Ensure it's an iterator and get the first field
    it = iter(it)
    try:
        prev = next(it)
    except StopIteration:
        return
    for item in it:
        # Lag by one item so I know I'm not at the end
        yield False, prev
        prev = item

    # Last item
    yield True, prev


def to_unsigned(val: int, width: int) -> int:
    if val < 0:
        mask = (1 << width) - 1
        return val & mask
    else:
        return val


def _mask_fits_hex(width: int, vld_mask: Optional[int]):
    # check bits for hex digit have all same value
    if not vld_mask:
        return True

    while width:
        m = vld_mask & 0xF
        if m != 0 and m != 0xF:
            return False
        vld_mask >>= 4
        width -= 4

    assert width == 0, ("Width should have been multiple of 4", width)
    return True


def bit_string(v: int, width: int, vld_mask:Optional[int]=None):
    """
    :param v: integer value of bitstring
    :param width: number of bits in value
    :param vld_mask: mask which has 1 for every valid bit in value
    :return: HdlValueInt
    """
    all_mask = (1 << width) - 1
    if v < 0:
        v = to_unsigned(v, width)

    if vld_mask is None:
        vld_mask = all_mask

    # if vld_mask == 0:
    #     if width % 4 == 0:
    #         base = 16
    #         bit_string = "".join(["x" for _ in range(width//4)])
    #     else:
    #         base = 2
    #         bit_string = "".join(["x" for _ in range(width)])
    widthFitsHexFormat = width % 4 == 0
    if vld_mask == (1 << width) - 1:
        # completely valid value
        if widthFitsHexFormat:
            # hex full valid
            base = 16
            bit_string = ("%0" + str(width // 4) + 'x') % (v)
        else:
            base = 2
            bit_string = ("{0:0" + str(width) + 'b}').format(v)
    else:
        buff = []
        if widthFitsHexFormat and _mask_fits_hex(width, vld_mask):
            # hex with some "x"
            base = 16
            for i in range(width - 4, -1, -4):
                mask = (1 << i)
                maskNibble = vld_mask & mask
                if maskNibble:
                    vNibble = v & mask
                    s = "%x" % (vNibble >> i)
                    assert len(s) == 1, s
                else:
                    s = "x"
                buff.append(s)

        else:
            # binary with some "x"
            base = 2
            for i in range(width - 1, -1, -1):
                mask = (1 << i)
                b = v & mask

                if vld_mask & mask:
                    s = "1" if b else "0"
                else:
                    s = "x"
                buff.append(s)
        bit_string = "".join(buff)
    return HdlValueInt(bit_string, width, base)
