from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render # Add
from editdatabase.sitelist.models import Site
from editdatabase.sitelist.models import Mouse
from editdatabase.sitelist.models import Fly
from editdatabase.sitelist.models import Human_Info
from editdatabase.sitelist.models import Mouse_Info
from editdatabase.sitelist.models import Fly_Info
import re
import sys
import os

def about(request):
	return render(request, 'about.html')

def download(request):
	return render(request, 'download.html')

def literature(request):
	return render(request, 'literature.html')

def contact(request):
	return render(request, 'contact.html')


def search(request):
	error_incorrectlocation = False
	error_toomanyresults = False
	error_nospecies = False
	if 'gene' in request.GET:
		gene = request.GET['gene']
		chrom = request.GET['chr']
		start = request.GET['start']
		end = request.GET['end']
		species = request.GET['species']
		query = "";
		if ((chrom or start or end) and (not chrom or not start or not end)): #check if incomplete genomic location
			error_incorrectlocation = True
		elif not species: #check if species is selected
			error_nospecies = True
		else:
			query = query + species + ' ';
			if (gene):
				if species == 'human':
					sites = Site.objects.filter(gene__iexact = gene)
				if species == 'mouse':
					sites = Mouse.objects.filter(gene__iexact = gene)
				if species == 'fly':
					sites = Fly.objects.filter(gene__iexact = gene)
				query = query + gene + ' ';
			elif (chrom):
				chrom = 'chr' + chrom
				if species == 'human':
					sites = Site.objects.filter(chrom__iexact = chrom, position__gte = start, position__lte = end)
				if species == 'mouse':
					sites = Mouse.objects.filter(chrom__iexact = chrom, position__gte = start, position__lte = end)
				if species == 'fly':
					sites = Fly.objects.filter(chrom__iexact = chrom, position__gte = start, position__lte = end)
				query = query + chrom + ':' + start + '-' + end + ' ';
			else:
				if species == 'human':
					sites = Site.objects.all()
				if species == 'mouse':
					sites = Mouse.objects.all()
				if species == 'fly':
					sites = Fly.objects.all()
			if (gene and chrom):
				chrom = 'chr' + chrom
				sites = sites.filter(chrom__iexact = chrom, position__gte = start, position__lte = end)
				query = query + chrom + ':' + start + '-' + end + ' ';

			if 'alu' in request.GET or 'repnonalu' in request.GET or 'nonrep' in request.GET:
				if not 'alu' in request.GET:
					sites = sites.exclude(alu__iexact = 'yes')
				if not 'repnonalu' in request.GET:
					sites = sites.exclude(repnonalu__iexact = 'yes')
				if not 'nonrep' in request.GET:
					sites = sites.exclude(alu__iexact = 'no', repnonalu__iexact = 'no')
				if 'alu' in request.GET:
					query = query + 'Alu ';
				if 'repnonalu' in request.GET:
					query = query + 'repetitive non-Alu ';
				if 'nonrep' in request.GET:
					query = query + 'non-repetitive ';

			if 'cons_human' in request.GET or 'cons_chimp' in request.GET or 'cons_rhesus' in request.GET or 'cons_mouse' in request.GET:
				if 'cons_human' in request.GET:
					sites = sites.exclude(human__isnull = True)
					query = query + 'Conservation_Human '
				if 'cons_chimp' in request.GET:
					sites = sites.exclude(chimp__isnull = True)
					query = query + 'Conservation_Chimpanzee '
				if 'cons_rhesus' in request.GET:
					sites = sites.exclude(rhesus__isnull = True)
					query = query + 'Conservation_Rhesus '
				if 'cons_mouse' in request.GET:
					sites = sites.exclude(mouse__isnull = True)
					query = query + 'Conservation_Mouse '

			if 'nonsyn' in request.GET or 'syn' in request.GET or '5utr' in request.GET or '3utr' in request.GET or 'ncrna' in request.GET or 'intronic' in request.GET or 'intergenic' in request.GET:
				if not 'syn' in request.GET:
					sites = sites.exclude(annot1__iexact = 'syn')
				if not 'nonsyn' in request.GET:
					sites = sites.exclude(annot1__iexact = 'nonsyn')
				if not '5utr' in request.GET:
					sites = sites.exclude(annot1__iexact = '5utr')
				if not '3utr' in request.GET:
					sites = sites.exclude(annot1__iexact = '3utr')
				if not 'ncrna' in request.GET:
					sites = sites.exclude(annot1__iexact = 'ncrna')
				if not 'intronic' in request.GET:
					sites = sites.exclude(annot1__iexact = 'intronic')
				if not 'intergenic' in request.GET:
					sites = sites.exclude(annot1__iexact = 'intergenic')
				if 'syn' in request.GET:
					query = query + 'synonymous ';
				if 'nonsyn' in request.GET:
					query = query + 'nonsynonymous ';
				if '5utr' in request.GET:
					query = query + '5\'UTR ';
				if '3utr' in request.GET:
					query = query + '3\'UTR ';
				if 'ncrna' in request.GET:
					query = query + 'ncRNA ';
				if 'intronic' in request.GET:
					query = query + 'intronic ';
				if 'intergenic' in request.GET:
					query = query + 'intergenic ';

			if sites.count() > 500:
				error_toomanyresults = True
			else:
				sites = sites.exclude(annot1__iexact = 'annot1')
				sites = sites.order_by("chrom","position")
				if species == 'human':
					genome = 'hg19'
				elif species == 'mouse':
					genome = 'mm9'
				elif species == 'fly':
					genome = 'dm3'
				for item in sites:
					item.genome = genome;
					location = item.chrom + ':' + item.position
					if species == 'human':
						searchpath = 'grep ' + location + ' /home/gokul/Gokul/editing_database/5-7-13/editome/ALLHUMAN_locations_uniq.py'; 
						if os.popen(searchpath).read():
							item.rnainfo = 'yes'
					if species == 'mouse':
						if Mouse_Info.objects.filter(name__iexact = location):
							item.rnainfo = 'yes'
					elif species == 'fly':
						if Fly_Info.objects.filter(name__iexact = location):
							item.rnainfo = 'yes' 

					RE_BILLY = re.compile(r'Billy')
					RE_BGI = re.compile(r'BGI')
					RE_DARNED = re.compile(r'DARNED')
					RE_KLEINMAN = re.compile(r'Kleinman')
					RE_NATMETH = re.compile(r'NatMeth')
					RE_UCLA = re.compile(r'UCLA')
					RE_PUBDAT = re.compile(r'PubDat')
					RE_PRIMATE = re.compile(r'Primate')
					RE_SANGER = re.compile(r'Sanger')
					RE_GRAVELEY = re.compile(r'Graveley')
					RE_RUI = re.compile(r'Rui')
					RE_NASCENTSEQ = re.compile(r'nascentseq')
					RE_CARMI = re.compile(r'Carmi')
					RE_SAKURAI = re.compile(r'Sakurai')
					RE_CHEPELEV = re.compile(r'Chepelev')
					RE_SOMMER = re.compile(r'Sommer')
					RE_GOMMANS = re.compile(r'Gommans')
					RE_LEVANON = re.compile(r'Levanon')
					RE_BHALLA = re.compile(r'Bhalla')
					RE_CLUTTERBUCK = re.compile(r'Clutterbuck')
					RE_BARBON = re.compile(r'Barbon')
					RE_OHLSON = re.compile(r'Ohlson')
					RE_NEEMAN = re.compile(r'Neeman')
					RE_BURNS = re.compile(r'Burns')
					if re.search(RE_BILLY, item.ref):
						item.ref2 = 'Li et al 2009'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/19478186"
					elif re.search(RE_DARNED, item.ref):
						item.ref2 = 'Kiran & Baranov 2010'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/20547637"
					elif re.search(RE_UCLA, item.ref):
						item.ref2 = 'Bahn et al 2012'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/21960545"
					elif re.search(RE_BGI, item.ref):
						item.ref2 = 'Peng et al 2012'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/22327324"
					elif re.search(RE_KLEINMAN, item.ref):
						item.ref2 = 'Kleinman, Adoue & Majewski 2012'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/22832026"
					elif re.search(RE_NATMETH, item.ref):
						item.ref2 = 'Ramaswami et al 2012'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/22484847"
					elif re.search(RE_PUBDAT, item.ref):
						item.ref2 = 'Ramaswami et al 2013'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/23291724"
					elif re.search(RE_PRIMATE, item.ref):
						item.ref2 = 'Ramaswami et al 2013'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/23291724"
					elif re.search(RE_SANGER, item.ref):
						item.ref2 = 'Danecek et al 2012'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/22524474"
					elif re.search(RE_GRAVELEY, item.ref):
						item.ref2 = 'Graveley et al 2011'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/21179090"
					elif re.search(RE_RUI, item.ref):
						item.ref2 = 'Ramaswami et al 2013'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/23291724"
					elif re.search(RE_NASCENTSEQ, item.ref):
						item.ref2 = 'Rodriguez, Menet & Rosbash 2012'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/22658416"
					elif re.search(RE_CARMI, item.ref):
						item.ref2 = 'Carmi, Borukhov & Levanon 2011'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/22028664"
					elif re.search(RE_SAKURAI, item.ref):
						item.ref2 = 'Sakurai et al. 2010'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/20835228"
					elif re.search(RE_CHEPELEV, item.ref):
						item.ref2 = 'Chepelev 2012'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/22130986"
					elif re.search(RE_SOMMER, item.ref):
						item.ref2 = 'Sommer et al. 1991'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/1717158"
					elif re.search(RE_GOMMANS, item.ref):
						item.ref2 = 'Gommans et al. 2008'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/18772245"
					elif re.search(RE_LEVANON, item.ref):
						item.ref2 = 'Levanon et al. 2005'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/15731336"
					elif re.search(RE_BHALLA, item.ref):
						item.ref2 = 'Bhalla et al. 2004'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/15361858"
					elif re.search(RE_CLUTTERBUCK, item.ref):
						item.ref2 = 'Clutterbuck et al. 2005'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/15797904"
					elif re.search(RE_BARBON, item.ref):
						item.ref2 = 'Barbon & Barlati 2000'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/10828597"
					elif re.search(RE_OHLSON, item.ref):
						item.ref2 = 'Ohlson et al. 2007'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/17369310"
					elif re.search(RE_NEEMAN, item.ref):
						item.ref2 = 'Neeman et al. 2006'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/16940548"
					elif re.search(RE_BURNS, item.ref):
						item.ref2 = 'Burns et al. 1997'
						item.ref3 = "http://www.ncbi.nlm.nih.gov/pubmed/9153397"
				return render(request, 'search_results.html', {'sites':sites, 'query':query})
	return render(request, 'search_form.html', {'error': error_incorrectlocation,'error2': error_toomanyresults,'error3': error_nospecies})

def additionalinfo(request):
	if 'genome' in request.GET:
		genome = request.GET['genome']
		location = request.GET['location']
		if genome == 'hg19':
			species = 'human';
			sites = Human_Info.objects.filter(name__iexact = location)
		elif genome == 'mm9':
			species = 'mouse';
			sites = Mouse_Info.objects.filter(name__iexact = location)
		elif genome == 'dm3':
			species = 'fly';
			sites = Fly_Info.objects.filter(name__iexact = location)
		return render(request, 'search_results_siteinfo.html', {'sites': sites, 'position' : location, 'species' : species})
	else:
		return render(request, 'search_results_siteinfo.html', {'position' : 'N/A', 'species' : 'N/A'})				
