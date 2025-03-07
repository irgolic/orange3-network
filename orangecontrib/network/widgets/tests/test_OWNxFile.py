import os
import unittest
from unittest.mock import patch, Mock

from orangecontrib.network.widgets.OWNxFile import OWNxFile
from orangecontrib.network.widgets.tests.utils import NetworkTest

TEST_NETS = os.path.join(os.path.split(__file__)[0], "networks")

def _get_test_net(filename):
    return os.path.join(TEST_NETS, filename)

class TestOWNxFile(NetworkTest):
    def setUp(self):
        self.widget = self.create_widget(OWNxFile)  # type: OWNxFile

    def test_read_error(self):
        with patch("orangecontrib.network.widgets.OWNxFile.read_pajek",
                   Mock(side_effect=OSError)):
            self.widget.open_net_file("foo.net")
        self.assertTrue(self.widget.Error.io_error.is_shown())
        filename = self._get_filename("leu_by_genesets.net")
        self.widget.open_net_file(filename)
        self.assertFalse(self.widget.Error.io_error.is_shown())

    def test_load_datafile(self):
        self.widget.open_net_file(_get_test_net("test.net"))
        items = self.get_output(self.widget.Outputs.items)
        self.assertEqual(items[0]["name"], "aaa")

    def test_invalid_datafile_length(self):
        # When data file's length does not match, the widget must create
        # a table from node labels
        self.widget.open_net_file(_get_test_net("test_inv.net"))
        self.assertTrue(self.widget.Warning.auto_mismatched_lengths)

        network = self.get_output(self.widget.Outputs.network)
        self.assertEqual(network.number_of_nodes(), 7)

        items = self.get_output(self.widget.Outputs.items)
        self.assertEqual(len(items), 7)
        self.assertEqual(items[0]["node_label"], "aa")


if __name__ == "__main__":
    unittest.main()
