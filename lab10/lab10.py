import re

def extractEmails(text):
    # Regex to extract valid email addresses
    email_pattern = re.compile(r"(?:^|\s)([\w.]+?@[\w]+\.[\w\.]+[\w])")
    emails = re.findall(email_pattern, text)
    return emails




def extractSimpsonInfo(html_text):
    # Regex to extract information about Simpson series
    simpson_pattern = re.compile(
        r"<td class=\"svtTablaTime\">\s+(\d+\.\d+)\s+</td>\s+"
        r"<td class=\"svtJsTablaShowInfo\">\s+"
        r"<h4 class=\"svtLink-hover svtTablaHeading\">\s+Simpsons\s+</h4>\s+"
        r"<div class=\"svtJsStopPropagation\">\s+"
        r"<div class=\"svtTablaTitleInfo svtHide-Js\">\s+"
        r"<div class=\"svtTablaContent-Description\">\s+"
        r"<p class=\"svtXMargin-Bottom-10px\">\s+Amerikansk animerad komediserie från [\d-]+\. Säsong (\d+)\. Del (\d+) av (\d+)\.(.+?)\s+</p>"
    )
    

    matches = re.findall(simpson_pattern, html_text)
    
    for match in matches:
        time, season, episode, description = match[0], match[1], f"{match[2]}\\{match[3]}", match[4]
        print("-" * 50)
        print(f"time: {time}\nseason: {season}\nepisode: {episode}\ndescription: {description}\n")

def main():
    # läsa och processa email infon
    email_text = "jox r.nohre@jth.hj.se, bjox@se, adam@example.com, jox@jox@jox.com."
    email_addresses = extractEmails(email_text)
    print("Email Addresses:")
    print(email_addresses)
    
    # Read and process Simpson information from HTML file
    with open("lab10/tabla.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        
        # Extracta och skriva ut alla tidpunkter
        time_points = re.findall(r'<td class="svtTablaTime">\s*(\d+\.\d+)\s*</td>', html_content)
        print("\nTime Points:")
        print(time_points)
        
    
    # Read and process Simpson information from HTML file
    with open("lab10/tabla.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        extractSimpsonInfo(html_content)

if __name__ == "__main__":
    main()
