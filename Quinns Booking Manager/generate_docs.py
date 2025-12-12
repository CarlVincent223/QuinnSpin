import webbrowser
import os

class write_docs_class:
    
    def __init__(self, ) -> None:
        pass

    def format_12hr(self, val):
        arr = val.split(' ')
        sub_arr = arr[1].split(':')
        if int(sub_arr[0]) == 0:
            sub_arr[0] = int(sub_arr[0])+12
            arr[1] = f"{sub_arr[0]}:{sub_arr[1]}:{sub_arr[2]}am"
        elif int(sub_arr[0]) > 12:
            sub_arr[0] = int(sub_arr[0])-12
            arr[1] = f"{sub_arr[0]}:{sub_arr[1]}:{sub_arr[2]}pm"
        else:
            arr[1] = f"{sub_arr[0]}:{sub_arr[1]}:{sub_arr[2]}am"

        return f"{arr[0]} {arr[1]}"

    def generate_customer_billing(self, data1, data2):
        temp_data = ""
        temp_data2 = ""
        temp_data3 = ""
        ctr = 0
        
        for entry in data1:
            if entry[0] == 'date':
                entry[1] = self.format_12hr(entry[1])

            if ctr == len(data1)-1:
                temp_data += f"\"{entry[0]}\":\"{entry[1]}\""
            else:
                temp_data += f"\"{entry[0]}\":\"{entry[1]}\","
            ctr+=1

        ctr = 0
        for entry in data2:
            if entry['prod_type'] == "addons":
                temp_data3 += "{"
                temp_data3 += f"\"name\":\"{entry['title']}\",\"price\":\"{entry['price']}\",\"qty\":\"{entry['quantity']}\",\"unit\":\"{entry['unit']}\",\"net_qty\":\"{entry['item_qty']}\""
                temp_data3 += "},"
            else:
                temp_data2 += "{"
                temp_data2 += f"\"name\":\"{entry['title']}\",\"price\":\"{entry['price']}\",\"qty\":\"{entry['quantity']}\",\"unit\":\"{entry['unit']}\",\"net_qty\":\"{entry['item_qty']}\""
                temp_data2 += "},"
            ctr+=1

        if temp_data2 == "":
            temp_data2 = temp_data2[0:len(temp_data2)-1]
        if temp_data3 == "":
            temp_data3 = temp_data3[0:len(temp_data3)-1]
        
        js_data = ""
        js_data += "function get_json_data(){ "
        js_data += "let data = {"
        js_data += temp_data
        js_data += "}; "
        js_data += "return data;"
        js_data += "} "

        js_data += ""
        js_data += "function get_json_data2(){ "
        js_data += "let data = ["
        js_data += temp_data2
        js_data += "]; "
        js_data += "return data;"
        js_data += "} "

        js_data += ""
        js_data += "function get_json_data3(){ "
        js_data += "let data = ["
        js_data += temp_data3
        js_data += "]; "
        js_data += "return data;"
        js_data += "} "

        #print(js_data)
        with open("assets/docs/billing_data.js", "w", encoding="utf-8") as file1:
            file1.write(js_data)
            file1.close()

        cwd = os.getcwd()
        webbrowser.open(f"{cwd}/assets/docs/billing.html", new=2)