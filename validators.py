import re


def normalize(_request):
    """This function is only to allow form data to be accepted (easier to test with Postman)"""
    try:
        data = _request.get_json()
    except:
        try:
            data = dict(_request.form)
        except:
            data = False
    return data


class PlateValidator(object):
    def __init__(self, response={}):
        self.response = response
        self.fields = ["plate"]

    def fields_check(self):
        """Checks for missing fields"""
        error_messages = []
        for field in self.fields:
            if self.response.get(field, None) is None:
                error_messages.append(f"Field '{field}' is required")
        return ". ".join(error_messages)

    def format_check(self):
        """For plate field check only"""
        valids = []
        err_msg = "Wrong plate format"
        parts = self.response.get("plate").split('-')
        if not parts or len(parts) != 2:
            return err_msg
        pattern = r"[A-Z]{1,3}"
        string = parts[0].strip()
        valids.append(bool(re.fullmatch(pattern, string)))
        # get numeric first
        num_part = re.findall(r'\d+', parts[1].strip())  # returns array
        if len(num_part) == 0 or len(num_part[0]) > 4:
            valids.append(False)
        if num_part[0][0] == 0 or num_part[0][0] == '0':
            valids.append(False)
        str_part = parts[1].strip().replace(num_part[0], '')
        pattern = r"[A-Z]{1,2}"
        valids.append(bool(re.fullmatch(pattern, str_part)))

        if not all(valids):
            return err_msg
