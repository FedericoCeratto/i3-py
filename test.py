import i3
import unittest
import platform
py3 = platform.python_version_tuple() > ('3',)

class ParseTest(unittest.TestCase):
    def setUp(self):
        self.msg_types = ['get_tree', 4, '4']
        self.event_types = ['output', 1, '1']
    
    def test_msg_parse(self):
        msg_types = []
        for msg_type in self.msg_types:
            msg_types.append(i3.parse_msg_type(msg_type))
        for index in range(-1, len(msg_types) - 1):
            self.assertEqual(msg_types[index], msg_types[index+1])
            self.assertIsInstance(msg_types[index], int)
    
    def test_event_parse(self):
        event_types = []
        for event_type in self.event_types:
            event_types.append(i3.parse_event_type(event_type))
        for index in range(-1, len(event_types) - 1):
            self.assertEqual(event_types[index], event_types[index+1])
            self.assertIsInstance(event_types[index], str)
    
    def test_msg_error(self):
        border_lower = -1
        border_higher = len(i3.msg_types)
        values = ['joke', border_lower, border_higher, -100, 100]
        for val in values:
            self.assertRaises(i3.MessageTypeError, i3.parse_msg_type, val)
            self.assertRaises(i3.MessageTypeError, i3.parse_msg_type, str(val))
    
    def test_event_error(self):
        border_lower = -1
        border_higher = len(i3.event_types)
        values = ['joke', border_lower, border_higher, -100, 100]
        for val in values:
            self.assertRaises(i3.EventTypeError, i3.parse_event_type, val)
            self.assertRaises(i3.EventTypeError, i3.parse_event_type, str(val))
    

class SocketTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_reponse(self):
        workspaces = i3.msg('get_workspaces')
        for workspace in workspaces:
            self.assertTrue('name' in workspace)
    
    def test_pack(self):
        packed = i3.default_socket().pack(0, "haha")
        if py3:
            self.assertIsInstance(packed, bytes)
    

class GeneralTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_getattr(self):
        func = i3.some_attribute
        self.assertTrue(callable(func))
        socket = i3.default_socket()
        self.assertIsInstance(socket, i3.Socket)
    
    def test_success(self):
        data = {'success': True}
        self.assertTrue(i3.success(data))
    

if __name__ == '__main__':
    for Test in [ParseTest, SocketTest, GeneralTest]:
        suite = unittest.TestLoader().loadTestsFromTestCase(Test)
        unittest.TextTestRunner(verbosity=2).run(suite)
