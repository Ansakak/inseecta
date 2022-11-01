
import numpy as np 
# import tensorflow as tf
from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg19 import VGG19, preprocess_input, decode_predictions
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array





app = Flask(__name__)


detailArray= [{"insectName":"ipynb_checkpoints", "chemicalName":"PROFENOFOS 500 g/l. EC", "ProductName":"CALCRON PROFENOFOS, HAYLEYS PROFENOFOS, CIC PROFENOPHOS, LANKEM PROFENOFOS, KUDUS PROFENOPHOS, PRODAN PROFENOPHOS, OASIS PROFENOPHOS", "path":"static/details/details_profenofos.jpg", "chem":"static/chemical/PROFENOFOS.jpg"},
       {"insectName":"Aleurocanthus spiniferus", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"Aphis citricola Vander Goot", "chemicalName":"FENOBUCARB 500 g/l EC", "ProductName":"DOZER FENOBUCARB, BASSA FENOBUCARB, HAYLEYS BPMC, CG BPMC, BEEPA FENOBUCARB, MACKCARB BPMC, DOZERR FENOBUCARB", "path":"static/details/details_bpmc.jpg", "chem":"static/chemical/BPMC.jpg" },
       {"insectName":"Cicadella viridis", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"Cicadellidae", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"Dacus dorsalis", "chemicalName":"PROFENOFOS 500 g/l. EC", "ProductName":"CALCRON PROFENOFOS, HAYLEYS PROFENOFOS, CIC PROFENOPHOS, LANKEM PROFENOFOS, KUDUS PROFENOPHOS, PRODAN PROFENOPHOS, OASIS PROFENOPHOS", "path":"static/details/details_profenofos.jpg", "chem":"static/chemical/PROFENOFOS.jpg"},
       {"insectName":"Dasineura sp", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"Icerya purchasi Maskell", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"Limacodidae", "chemicalName":"THIAMETHOXAM 20% + CHLORANTRANILIPROLE 20% (w/w) WG", "ProductName":"VIRTAKO 40 WG", "path":"static/details/details_virtako.jpg", "chem":"static/chemical/CIC_VIRTACO.jpg"},
       {"insectName":"Locustoidea", "chemicalName":"PROFENOFOS 500 g/l. EC", "ProductName":"CALCRON PROFENOFOS, HAYLEYS PROFENOFOS, CIC PROFENOPHOS, LANKEM PROFENOFOS, KUDUS PROFENOPHOS, PRODAN PROFENOPHOS, OASIS PROFENOPHOS", "path":"static/details/details_profenofos.jpgstatic/details/details_profenofos.jpg", "chem":"static/chemical/PROFENOFOS.jpg"},
       {"insectName":"Papilio xuthus", "chemicalName":"PROFENOFOS 500 g/l. EC", "ProductName":"CALCRON PROFENOFOS, HAYLEYS PROFENOFOS, CIC PROFENOPHOS, LANKEM PROFENOFOS, KUDUS PROFENOPHOS, PRODAN PROFENOPHOS, OASIS PROFENOPHOS", "path":"static/details/details_profenofos.jpg", "chem":"static/chemical/PROFENOFOS.jpg"},
       {"insectName":"Phyllocnistis citrella Stainton", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"Pieris canidia", "chemicalName":"FENOBUCARB 500 g/l EC", "ProductName":"DOZER FENOBUCARB, BASSA FENOBUCARB, HAYLEYS BPMC, CG BPMC, BEEPA FENOBUCARB, MACKCARB BPMC, DOZERR FENOBUCARB", "path":"static/details/details_bpmc.jpg", "chem":"static/chemical/BPMC.jpg"},
       {"insectName":"Potosiabre vitarsis", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"Prodenia litura", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
       {"insectName":"Rhytidodera bowrinii white", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
       {"insectName":"Rice Stemfly", "chemicalName":"PROTEIN BAIT + SPINOSAD 25 g/l SC", "ProductName":"LakGro Bait", "path":"static/details/details_lakgow.jpg", "chem":"static/chemical/LAKGROWBAIT.jpg"},
       {"insectName":"Salurnis marginella Guerr", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"Scirtothrips dorsalis Hood", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"Thrips", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"Trialeurodes vaporariorum", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"Unaspis yanonensis", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"Viteus vitifoliae", "chemicalName":"THIAMETHOXAM 20% + CHLORANTRANILIPROLE 20% (w/w) WG", "ProductName":"VIRTAKO 40 WG", "path":"static/details/details_virtako.jp", "chem":"static/chemical/CIC_VIRTACO.jpg"},
       {"insectName":"alfalfa plant bug", "chemicalName":"FENOBUCARB 500 g/l EC", "ProductName":"DOZER FENOBUCARB, BASSA FENOBUCARB, HAYLEYS BPMC, CG BPMC, BEEPA FENOBUCARB, MACKCARB BPMC, DOZERR FENOBUCARB", "path":"static/details/details_bpmc.jpg", "chem":"static/chemical/BPMC.jpg"},
       {"insectName":"aphids", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"army worm", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
       {"insectName":"beet army worm", "chemicalName":"THIAMETHOXAM 20% + CHLORANTRANILIPROLE 20% (w/w) WG", "ProductName":"VIRTAKO 40 WG", "path":"static/details/details_virtako.jp", "chem":"static/chemical/CIC_VIRTACO.jpg"},
       {"insectName":"bird cherry-oataphid", "chemicalName":"FENOBUCARB 500 g/l EC", "ProductName":"DOZER FENOBUCARB, BASSA FENOBUCARB, HAYLEYS BPMC, CG BPMC, BEEPA FENOBUCARB, MACKCARB BPMC, DOZERR FENOBUCARB", "path":"static/details/details_bpmc.jpg", "chem":"static/chemical/BPMC.jpg"},
       {"insectName":"black cutworm", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
       {"insectName":"blister beetle", "chemicalName":"FENOBUCARB 500 g/l EC", "ProductName":"DOZER FENOBUCARB, BASSA FENOBUCARB, HAYLEYS BPMC, CG BPMC, BEEPA FENOBUCARB, MACKCARB BPMC, DOZERR FENOBUCARB", "path":"static/details/details_bpmc.jpg", "chem":"static/chemical/BPMC.jpg"},
       {"insectName":"cabbage army worm", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
       {"insectName":"corn borer", "chemicalName":"THIAMETHOXAM 20% + CHLORANTRANILIPROLE 20% (w/w) WG", "ProductName":"VIRTAKO 40 WG", "path":"static/details/details_virtako.jp", "chem":"static/chemical/CIC_VIRTACO.jpg"},
       {"insectName":"english grain aphid", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"flea beetle", "chemicalName":"PROFENOFOS 500 g/l. EC", "ProductName":"CALCRON PROFENOFOS, HAYLEYS PROFENOFOS, CIC PROFENOPHOS, LANKEM PROFENOFOS, KUDUS PROFENOPHOS, PRODAN PROFENOPHOS, OASIS PROFENOPHOS", "path":"static/details/details_profenofos.jpg", "chem":"static/chemical/PROFENOFOS.jpg"},
       {"insectName":"grub", "chemicalName":"THIAMETHOXAM 20% + CHLORANTRANILIPROLE 20% (w/w) WG", "ProductName":"VIRTAKO 40 WG", "path":"static/details/details_virtako.jp", "chem":"static/chemical/CIC_VIRTACO.jpg"},
       {"insectName":"mole cricket", "chemicalName":"PROFENOFOS 500 g/l. EC", "ProductName":"CALCRON PROFENOFOS, HAYLEYS PROFENOFOS, CIC PROFENOPHOS, LANKEM PROFENOFOS, KUDUS PROFENOPHOS, PRODAN PROFENOPHOS, OASIS PROFENOPHOS", "path":"static/details/details_profenofos.jpg", "chem":"static/chemical/PROFENOFOS.jpg"},
       {"insectName":"oides decempunctata", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"red spider", "chemicalName":"FENOBUCARB 500 g/l EC", "ProductName":"DOZER FENOBUCARB, BASSA FENOBUCARB, HAYLEYS BPMC, CG BPMC, BEEPA FENOBUCARB, MACKCARB BPMC, DOZERR FENOBUCARB", "path":"static/details/details_bpmc.jpg", "chem":"static/chemical/BPMC.jpg"},
       {"insectName":"small brown plant hopper", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
       {"insectName":"tarnished plant bug", "chemicalName":"ABAMECTIN 18 g/l EC", "ProductName":"MITSU ABAMECTIN, CIC ABAMECTIN, ABA ABAMECTIN, CG ABAMECTIN, ICS ABAMECTIN, ZORO ABAMECTIN, MIGHTEE ABAMECTIN", "path":"static/details/details_abamectin.jpg", "chem":"static/chemical/ABAMECTIN.jpg"},
       {"insectName":"wheat blossom midge", "chemicalName":"PROFENOFOS 500 g/l. EC", "ProductName":"CALCRON PROFENOFOS, HAYLEYS PROFENOFOS, CIC PROFENOPHOS, LANKEM PROFENOFOS, KUDUS PROFENOPHOS, PRODAN PROFENOPHOS, OASIS PROFENOPHOS", "path":"static/details/details_profenofos.jpg", "chem":"static/chemical/PROFENOFOS.jpg"},
       {"insectName":"wheat sawfly", "chemicalName":"PROTEIN BAIT + SPINOSAD 25 g/l SC", "ProductName":"LakGro Bait", "path":"static/details/details_lakgow.jpg", "chem":"static/chemical/LAKGROWBAIT.jpg"},
       {"insectName":"white backed plant hopper", "chemicalName":"IMIDACLOPRID 200 g/l SL", "ProductName":"ADMIRE IMIDACLOPRID, SUN AGRO IMIDACLOPRID, IMIDA IMIDACLOPRID, MERIT IMIDACLOPRID, DYNAMIC IMIDACLOPRID, TATAMIDA IMIDACLOPRID,", "path":"static/details/details_imida.jpg", "chem":"static/chemical/IMIDA.jpg"},
       {"insectName":"wireworm", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
       {"insectName":"yellow cutworm", "chemicalName":"FIPRONIL 50 g/l SC", "ProductName":"REGENT 50 SC, ZEES FIPRONIL, DIFENDER FIPRONIL, GRAND FIPRONIL, CG FIPRONIL, VIPER FIPRONIL, ARREARS FIPRONIL, FIPROGEN FIPRONIL , RIO FIPRONIL", "path":"static/details/deatils_fipronil.jpg", "chem":"static/chemical/FIPRONIL.jpg"},
	   {"insectName":"yellow rice borer", "chemicalName":"THIAMETHOXAM 20% + CHLORANTRANILIPROLE 20% (w/w) WG", "ProductName":"VIRTAKO 40 WG", "path":"static/details/details_virtako.jp", "chem":"static/chemical/CIC_VIRTACO.jpg"}
      
       ]
dic = {
	0 : 'ipynb_checkpoints',
	1 : 'Aleurocanthus spiniferus',
	2 : 'Aphis citricola Vander Goot',
	3 : 'Cicadella viridis',
	4 : 'Cicadellidae',
	5 : 'Dacus dorsalis',
	6 : 'Dasineura sp',
	7 : 'Icerya purchasi Maskell',
	8 : 'Limacodidae',
	9 : 'Locustoidea',
	10 : 'Papilio xuthus',
	11 : 'Phyllocnistis citrella Stainton',
	12 : 'Pieris canidia',
	13 : 'Potosiabre vitarsis',
	14 : 'Prodenia litura',
	15 : 'Rhytidodera bowrinii white',
	16 : 'Rice Stemfly',
	17 : 'Salurnis marginella Guerr',
	18 : 'Scirtothrips dorsalis Hood',
	19 : 'Thrips',
	20 : 'Trialeurodes vaporariorum',
	21 : 'Unaspis yanonensis',
	22 : 'Viteus vitifoliae',
	23 : 'alfalfa plant bug',
	24 : 'aphids',
	25 : 'army worm',
	26 : 'beet army worm',
	27 : 'bird cherry-oataphid',
	28 : 'black cutworm',
	29 : 'blister beetle',
	30 : 'cabbage army worm',
	31 : 'corn borer',
	32 : 'english grain aphid',
	33 : 'flea beetle',
	34 : 'grub',
	35 : 'mole cricket',
	36 : 'oides decempunctata',
	37 : 'red spider',
	38 : 'small brown plant hopper',
	39 : 'tarnished plant bug',
	40 : 'wheat blossom midge',
	41 : 'wheat sawfly',
	42 : 'white backed plant hopper',
	43 : 'wireworm',
	44 : 'yellow cutworm',
	45 : 'yellow rice borer'
	}

   
model = load_model('best_model.h5')

model.make_predict_function()

def predict_label(img_path):    
	i = load_img(img_path, target_size=(256,256))
	im = img_to_array(i)
	img = np.expand_dims(im , axis=0)
	pred = np.argmax(model.predict(img) ) 	
	return dic[pred]    
   
	


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)
	filteredDetai= list(filter(lambda x:x["insectName"]==p,detailArray))	
	return render_template("index.html", prediction = p, img_path = img_path,filteredDetai = filteredDetai)


if __name__ =='__main__':
	#app.debug = True
	app.run(host="0.0.0.0", port=3000)
