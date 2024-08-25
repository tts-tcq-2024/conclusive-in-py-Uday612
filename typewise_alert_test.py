import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):
  def test_infer_breach(self):
    self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
    self.assertTrue(typewise_alert.infer_breach(50, 50, 100) == 'NORMAL')
    self.assertTrue(typewise_alert.infer_breach(110, 50, 100) == 'TOO_HIGH')

  def test_get_upper_limit(self):
    self.assertTrue(typewise_alert.get_upper_limit('PASSIVE_COOLING') == 35)
    self.assertTrue(typewise_alert.get_upper_limit('HI_ACTIVE_COOLING') == 45)
    self.assertTrue(typewise_alert.get_upper_limit('MED_ACTIVE_COOLING') == 40)

  def test_classify_temperature_breach(self):
    self.assertTrue(typewise_alert.classify_temperature_breach("PASSIVE_COOLING",35) == 'NORMAL')
    self.assertTrue(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING",45) == 'NORMAL')
    self.assertTrue(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING",40) == 'NORMAL')
    self.assertTrue(typewise_alert.classify_temperature_breach("PASSIVE_COOLING",-1) == 'TOO_LOW')
    self.assertTrue(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING",-2) == 'TOO_LOW')
    self.assertTrue(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING",-3) == 'TOO_LOW')
    self.assertTrue(typewise_alert.classify_temperature_breach("PASSIVE_COOLING",40) == 'TOO_HIGH')
    self.assertTrue(typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING",50) == 'TOO_HIGH')
    self.assertTrue(typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING",45) == 'TOO_HIGH')

  @patch('__main__.print_message')
  def test_send_to_controller_normal(self, mock_print_message):
    send_to_controller('NORMAL')
    mock_print_message.assert_called_with('65261, NORMAL')

  @patch('__main__.print_message')
  def test_send_to_controller_too_high(self, mock_print_message):
    end_to_controller('TOO_HIGH')
    mock_print_message.assert_called_with('65261, TOO_HIGH')

  @patch('__main__.print_message')
  def test_send_to_email_too_low(self, mock_print_message):
    send_to_email('TOO_LOW')
    mock_print_message.assert_called_with('To: a.b@c.com\nHi, the temperature is too low')

  @patch('__main__.print_message')
  def test_send_to_email_too_high(self, mock_print_message):
    send_to_email('TOO_HIGH')
    mock_print_message.assert_called_with('To: a.b@c.com\nHi, the temperature is too high')

  @patch('__main__.send_to_controller')
  def test_check_and_alert_to_controller_normal(self, mock_send_to_controller):
    batteryChar = {'coolingType': 'PASSIVE_COOLING'}
    check_and_alert('TO_CONTROLLER', batteryChar, 25)
    mock_send_to_controller.assert_called_with('NORMAL')

  @patch('__main__.send_to_controller')
  def test_check_and_alert_to_controller_too_high(self, mock_send_to_controller):
    batteryChar = {'coolingType': 'PASSIVE_COOLING'}
    check_and_alert('TO_CONTROLLER', batteryChar, 45)
    mock_send_to_controller.assert_called_with('TOO_HIGH')

  @patch('__main__.send_to_email')
  def test_check_and_alert_to_email_too_low(self, mock_send_to_email):
    batteryChar = {'coolingType': 'HI_ACTIVE_COOLING'}
    check_and_alert('TO_EMAIL', batteryChar, -10)
    mock_send_to_email.assert_called_with('TOO_LOW')

  @patch('__main__.send_to_email')
  def test_check_and_alert_to_email_too_high(self, mock_send_to_email):
    batteryChar = {'coolingType': 'MED_ACTIVE_COOLING'}
    check_and_alert('TO_EMAIL', batteryChar, 50)
    mock_send_to_email.assert_called_with('TOO_HIGH')

  @patch('__main__.send_to_email')
  def test_check_and_alert_normal_email(self, mock_send_to_email):
    batteryChar = {'coolingType': 'HI_ACTIVE_COOLING'}
    check_and_alert('TO_EMAIL', batteryChar, 30)
    mock_send_to_email.assert_called_with('NORMAL')

if __name__ == '__main__':
  unittest.main()
