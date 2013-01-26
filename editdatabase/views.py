from django.http import HttpResponse
from django.shortcuts import render_to_response
from editdatabase.sitelist.models import Site
from editdatabase.sitelist.models import Mouse
from editdatabase.sitelist.models import Fly
import re

def about(request):
	return render_to_response('about.html')

def download(request):
	return render_to_response('download.html')

def literature(request):
	return render_to_response('literature.html')

def contact(request):
	return render_to_response('contact.html')


def search(request):
	error = False
	error2 = False
	error3 = False
	if 'gene' in request.GET:
		gene = request.GET['gene']
		chrom = request.GET['chr']
		start = request.GET['start']
		end = request.GET['end']
		species = request.GET['species']
		query = "";
		if ((chrom or start or end) and (not chrom or not start or not end)):
			error = True
		elif not species:
			error3 = True
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
			if sites.count() > 5000:
				error2 = True
			else:
				sites = sites.exclude(annot1__iexact = 'annot1')
				sites = sites.order_by("chrom","position")
				for item in sites:
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
				return render_to_response('search_results.html', {'sites':sites, 'query':query})
	return render_to_response('search_form.html', {'error': error,'error2': error2,'error3': error3})
