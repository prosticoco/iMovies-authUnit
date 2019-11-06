import argparse




































def main(args):
	controller = Controller(args.challenge,args.dir,
							args.record,args.domain,args.revoke)
	controller.run_acme()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('challenge',choices = ['dns01','http01'],
		help = 'ACME challenge type')
	parser.add_argument('--dir', required = True)
	parser.add_argument('--record',required = True)
	parser.add_argument('--domain', required = True, action='append')
	parser.add_argument('--revoke', action= 'store_true')
	arguments = parser.parse_args()
	main(arguments)


