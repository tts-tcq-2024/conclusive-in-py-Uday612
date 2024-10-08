import unittest
from unittest.mock import patch
from typewise_alert import infer_breach, get_upper_limit, classify_temperature_breach, check_and_alert, send_to_controller, send_to_email, print_message


class TypewiseTest(unittest.TestCase):
  def test_infer_breach(self):
    self.assertTrue(infer_breach(20, 50, 100) == 'TOO_LOW')
    self.assertTrue(infer_breach(50, 50, 100) == 'NORMAL')
    self.assertTrue(infer_breach(110, 50, 100) == 'TOO_HIGH')

  def test_get_upper_limit(self):
    self.assertTrue(get_upper_limit('PASSIVE_COOLING') == 35)
    self.assertTrue(get_upper_limit('HI_ACTIVE_COOLING') == 45)
    self.assertTrue(get_upper_limit('MED_ACTIVE_COOLING') == 40)

  def test_classify_temperature_breach(self):
    self.assertTrue(classify_temperature_breach("PASSIVE_COOLING",35) == 'NORMAL')
    self.assertTrue(classify_temperature_breach("HI_ACTIVE_COOLING",45) == 'NORMAL')
    self.assertTrue(classify_temperature_breach("MED_ACTIVE_COOLING",40) == 'NORMAL')
    self.assertTrue(classify_temperature_breach("PASSIVE_COOLING",-1) == 'TOO_LOW')
    self.assertTrue(classify_temperature_breach("HI_ACTIVE_COOLING",-2) == 'TOO_LOW')
    self.assertTrue(classify_temperature_breach("MED_ACTIVE_COOLING",-3) == 'TOO_LOW')
    self.assertTrue(classify_temperature_breach("PASSIVE_COOLING",40) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach("HI_ACTIVE_COOLING",50) == 'TOO_HIGH')
    self.assertTrue(classify_temperature_breach("MED_ACTIVE_COOLING",45) == 'TOO_HIGH')

  @patch('builtins.print')
  def test_send_to_controller(self, mock_print):
    send_to_controller('NORMAL')
    mock_print.asser_called_with('65261, NORMAL')
    send_to_controller('TOO_LOW')
    mock_print.asser_called_with('65261, TOO_LOW')
    send_to_controller('TOO_HIGH')
    mock_print.asser_called_with('65261, TOO_HIGH')

  @patch('builtins.print')
  def test_send_to_email(self, mock_print):
    send_to_email('TOO_LOW')
    mock_print.assert_called_with('To: a.b@c.com\nHi, the temperature is TOO_LOW')
    send_to_email('TOO_HIGH')
    mock_print.assert_called_with('To: a.b@c.com\nHi, the temperature is TOO_HIGH')
    send_to_email('NORMAL')
    mock_print.assert_called_with('To: a.b@c.com\nHi, the temperature is NORMAL')

  @patch('builtins.print')
  def test_check_and_alert_to_controller(self, mock_print):
    batteryChar = {'coolingType': 'PASSIVE_COOLING'}
    check_and_alert('TO_CONTROLLER', batteryChar, 25)
    mock_print.asser_called_with('65261, NORMAL')
    batteryChar = {'coolingType': 'HI_ACTIVE_COOLING'}
    check_and_alert('TO_CONTROLLER', batteryChar, -5)
    mock_print.asser_called_with('65261, TOO_LOW')
    batteryChar = {'coolingType': 'MED_ACTIVE_COOLING'}
    check_and_alert('TO_CONTROLLER', batteryChar, 50)
    mock_print.asser_called_with('65261, TOO_HIGH')

  @patch('builtins.print')
  def test_check_and_alert_to_email(self, mock_print):
    batteryChar = {'coolingType': 'HI_ACTIVE_COOLING'}
    check_and_alert('TO_EMAIL', batteryChar, -10)
    mock_print.assert_called_with('To: a.b@c.com\nHi, the temperature is TOO_LOW')
    batteryChar = {'coolingType': 'MED_ACTIVE_COOLING'}
    check_and_alert('TO_EMAIL', batteryChar, 50)
    mock_print.assert_called_with('To: a.b@c.com\nHi, the temperature is TOO_HIGH')
    batteryChar = {'coolingType': 'HI_ACTIVE_COOLING'}
    check_and_alert('TO_EMAIL', batteryChar, 30)
    mock_print.assert_called_with('To: a.b@c.com\nHi, the temperature is NORMAL')

  @patch('builtins.print')
  def test_print_message(self, mock_print):
    print_message('Bosch')
    mock_print.assert_called_with('Bosch')
    
if __name__ == '__main__':
  unittest.main()
