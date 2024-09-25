import argparse
import datetime
import json
import os
import urllib.request

DOC = """
<!doctype html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8">
	<meta http-equiv="refresh" content="30"/>
	<title>Tiny Monitor</title>
	<link
		rel="stylesheet"
		href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css"
	>
</head>

<body>
	<header>
		<hgroup>
			<h1>Tiny Monitor</h1>
			<p>A small uptime monitor, by @joefg</p>
		</hgroup>
	</header>

	<main>
		<section id="services">
				<h2>Services</h2>
				<table>
						<thead>
								<tr>
										<th>Service</th>
										<th>Status</th>
								</tr>
								</thead>
						<tbody>
                            {table_rows}
						</tbody>
				</table>
		</section>
	</main>
    <footer>
        Last updated: {time}
    </footer>
</body>
</html>
"""

def get_service_statuses(config):
    services = []

    with open(os.path.join(config), 'r') as cfg:
        services = json.loads(cfg.read())['services']
    
    for service in services:
        try:
            r = urllib.request.urlopen(service['url'])
            service['response'] = r.code
        except Exception as e:
            service['response'] = e

    return services

def build_document(statuses):
    table_rows = ""
    
    for status in statuses:
        ret = f"""
            <tr>
                <td>{status['url']}</td>
                <td>{status['response']}</td>
            </tr>
        """
        table_rows += ret

    time = str(datetime.datetime.now())
    return DOC.format(table_rows=table_rows, time=time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Tiny Monitor"
    )
    parser.add_argument('-c', '--config', required=True)
    args = parser.parse_args()

    statuses = get_service_statuses(args.config)
    doc = build_document(statuses)
    print(doc)
