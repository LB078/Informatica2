from unittest import TestCase, main
from namehasher import (
    set_dict_key,
    encode_string,
    decode_string,
    encode_list,
    decode_list,
    validate_values,
)


class TestStringMethods(TestCase):

    def test_encode_string(self):
        set_dict_key(
            "a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$"
        )

        self.assertEqual("6<= </ 117 =1/=", encode_string("dit is een test"))
        self.assertEqual("%<= [/ #17 T1/=", encode_string("Dit Is Een Test"))

    def test_decode_string(self):
        set_dict_key(
            "a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$"
        )

        self.assertEqual("dit is een test", decode_string("6<= </ 117 =1/="))
        self.assertEqual("Dit Is Een Test", decode_string("%<= [/ #17 T1/="))

    def test_encode_list(self):
        set_dict_key(
            "a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$"
        )

        self.assertEqual(
            ["6<= </ 117 =1/=", "%<= [/ #17 T1/="],
            encode_list(["dit is een test", "Dit Is Een Test"]),
        )

    def test_decode_list(self):
        set_dict_key(
            "a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$"
        )

        self.assertEqual(
            ["dit is een test", "Dit Is Een Test"],
            decode_list(["6<= </ 117 =1/=", "%<= [/ #17 T1/="]),
        )

    def test_validate_values(self):
        set_dict_key(
            "a_b?c9d6e1f4g!h:i<j|k{l0m@n7o+p~q2r+s/t=u^v3w]x(y-z>A*B8C;D%E#F}G5H)I[J$"
        )

        self.assertEqual(True, validate_values("6<= </ 117 =1/=", "dit is een test"))
        self.assertEqual(True, validate_values("%<= [/ #17 T1/=", "Dit Is Een Test"))


if __name__ == "__main__":
    main()
