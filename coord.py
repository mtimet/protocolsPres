import pandas as pd

if __name__ == "__main__":
	fout = 'csvout/aggregate_with_coordinates.csv'
	agg = pd.read_csv('csvout/aggregate.csv')
	centers = pd.read_csv('pollingCenters.csv')

	mm = pd.merge(agg,centers, how='left', left_on='center_name', right_on='center_name_ar')
	mm.to_csv(fout,index=False)
	print('END. file generated :', fout )