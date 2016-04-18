


import os,string,math,sys


try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))
    
from dxfwrite import DXFEngine as dxf
from dxfwrite.const import CENTER, RIGHT, ALIGNED, FIT, BASELINE_MIDDLE
from dxfwrite.const import TOP, MIDDLE, BOTTOM




radArcMin=1
colorLine= 0#0:black 1:red 2:yellow 7:white
colorText=1
shiftTopLineText= 2.5 
sizeText=radArcMin * 5
currentLayer='layer1'
space=radArcMin * 2
#------------------------------------------
centroX=148.5
centroY=105
shiftLetras=5.771
GradosAño=12
GradosMes=1
colorLine2=1
colorLine3=3
colorLine4=4
colorLine5=5
colorLine6=6
colorLine7=8
#------------------------------------------
def dameCuadrante(ang):
	numCuadrante=1
	if ang <= 90:
		numCuadrante=1
	elif ang > 90 and ang <= 180:
		numCuadrante=2
	elif ang > 180 and ang <=270:
		numCuadrante=3
	else:
		numCuadrante=4
	return numCuadrante

def traduceElAnguloRelojATrigonometria(angO):
#pre: el angulo que esta en ang0 se basa  en las 12 del reloj
#post: se devuelve el valor de un angulo correspondiente los angulos matematicos partiendo del eje X  hacia la izquierda
#360 + 90=450 
	angD=450 - angO
	if angD > 360:
		angD = angD -360
	if angD < 0:
		angD=360 + angD
	return angD

def damePtoArcoReloj(xCenter,yCenter,ang,radio):
#pre: x e y del cetro del arco
#una angulo en grados y un radio
#post: devuelve el otro punto extremo de la hipotenusa
	'''
	print ("el radio es: ",radio)
	print ("el anguloOriginal es:",ang) 
	'''
	ang=traduceElAnguloRelojATrigonometria(ang)
#	print ("el anguloReal es:",ang) 
	cuad=dameCuadrante(ang)
	'''
	print ("el cuadrante del angulo real es:",cuad)
	print ("este es el coseno de ang",math.cos(math.radians(ang)))
	print ("este es el seno de ang",math.sin(math.radians(ang)))
	'''
	a=math.cos(math.radians(ang))* radio #math.cos acepta radianes solo
	b=math.sin(math.radians(ang))* radio #math.sin acepta radianes solo
	if cuad==1:
		'''
		print ("este es el angulo de calculo",ang)
		print ("este es el coseno de ang",math.cos(math.radians(ang)))
		print ("este es el seno de ang",math.sin(math.radians(ang)))
		'''
		a=math.cos(math.radians(ang))* radio #math.cos acepta radianes solo
		b=math.sin(math.radians(ang))* radio #math.sin acepta radianes solo
		xd=xCenter + a
		yd=yCenter + b
	elif cuad==2:
		ang=180-ang#complementario
		'''
		print ("este es el angulo de calculo",ang)
		print ("este es el coseno de ang",math.cos(math.radians(ang)))
		print ("este es el seno de ang",math.sin(math.radians(ang)))
		'''
		a=math.cos(math.radians(ang))* radio #math.cos acepta radianes solo
		b=math.sin(math.radians(ang))* radio #math.sin acepta radianes solo
		xd=xCenter - a
		yd=yCenter + b
	elif cuad==3:
		ang=ang-180
		'''
		print ("este es el angulo de calculo",ang)
		print ("este es el coseno de ang",math.cos(math.radians(ang)))
		print ("este es el seno de ang",math.sin(math.radians(ang)))
		'''
		a=math.cos(math.radians(ang))* radio #math.cos acepta radianes solo
		b=math.sin(math.radians(ang))* radio #math.sin acepta radianes solo
		xd=xCenter - a
		yd=yCenter - b
	else:#cuad=4
		ang=360-ang
		'''
		print ("este es el angulo de calculo",ang)
		print ("este es el coseno de ang",math.cos(math.radians(ang)))
		print ("este es el seno de ang",math.sin(math.radians(ang)))
		'''
		a=math.cos(math.radians(ang))* radio #math.cos acepta radianes solo
		b=math.sin(math.radians(ang))* radio #math.sin acepta radianes solo
		xd=xCenter + a
		yd=yCenter - b
	'''
	print ("esto es el tamaño del lado adyacente:",a)
	print ("esto es el tamaño del lado opuesto:",b)
	'''
	return xd,yd

# def escribeEnArco(draw,texto,centroX,centroY,base,anguloIni,anguloFin,color,tamFte):
	# #writeTextNoAling(draw,txt,px0,py0,size,colorTextt,layerTxt,angRotation)
	# numLetras=len(texto)
	# numGrados=anguloFin-anguloIni
	# angIni=traduceElAnguloRelojATrigonometria(anguloIni)
	# # if numletras < numGrados:	
	# ratio=numGrados/numLetras
	# angSig=angIni+ratio
	# for i in range(numLetras):
		# angSig=angSig+ratio
		# px0,py0=damePtoArcoReloj(centroX,centroY,angSig,base)
		# writeTextNoAling(draw,texto[i],px0,py0,tamFte,color,currentLayer,angSig)
	# #writeTextNoAling(draw,'universidad',px0,py0,12,5,currentLayer,0)
	# draw.save()

def dameGradosRotacionTexto(anguloIni,anguloFin):
	angDef=((anguloIni+anguloFin)/2)+270.0
	if(angDef > 360.0):
		print ("resultado es un angulo mayor de 360")
		angDef = angDef - 360.0
	return angDef

def posicionaTexto(angIni,angFin,xCenter,yCenter,radio):
	ang =(angIni+angFin)/2
	x,y = damePtoArcoReloj(xCenter,yCenter,ang,radio)
	return x,y

def testeaAlineacionLetras(draw,angIni,angFin,xCenter,yCenter,radio,color,capa):
	#pre:
	#post: dibuja una linea por donde se debiera alinear el texto perpendicularmente a ella
	x,y = posicionaTexto(angIni,angFin,xCenter,yCenter,radio)
	drawLineColouredLayer(draw,xCenter,yCenter,x,y,color,capa)

def escribeEnArcoCapa(draw,texto,xCenter,yCenter,anguloIni,anguloFin,radio,color,tamFte,capa,espejo=0):
#pre: espejo valor 0,1,2
#post: espejo=0 sin mirror, espejo=1 con mirror en X, espejo=2 con mirror en Y
#		anguloIni, anguloFin son angulos como el reloj desde las 12
	print ("este es el angulo inicial:",anguloIni)
	print ("este es el angulo final:",anguloFin)
	anIni = traduceElAnguloRelojATrigonometria(anguloIni)
	anFin = traduceElAnguloRelojATrigonometria(anguloFin)
	print ("este es el angulo calculo inicial:",anIni)
	print ("este es el angulo calculo final:",anFin)
	rot = dameGradosRotacionTexto(anIni,anFin)
	print ("EL ANGULO DE ROTACION DEL TEXTO ES :",rot)
	pX,pY=posicionaTexto(anguloIni,anguloFin,xCenter,yCenter,radio)#importante el angulo es de reloj
	text = dxf.mtext(texto,(pX,pY))
	text.layer = capa
	text.color = color
	text.height = tamFte
	text.rotation = rot
	text.halign = dxfwrite.CENTER
##	text.halign = dxfwrite.ALIGNED
	if (espejo != 0):
		if (espejo == 1):
			text.mirror = dxfwrite.MIRROR_X
		else:
			text.mirror = dxfwrite.MIRROR_Y
	draw.add(text)
	draw.save()

def dibujaArcoRelojColoreadoCapa(draw,centroX,centroY,base,anguloIni,anguloFin,colorLine2,capa): 
	angI=traduceElAnguloRelojATrigonometria(anguloIni)
	angF=traduceElAnguloRelojATrigonometria(anguloFin)
	drawArcColouredLayer(draw,centroX,centroY,base,angF,angI,colorLine2,capa)
 
def dibujaArcoRelojColoreado(draw,centroX,centroY,base,anguloIni,anguloFin,colorLine2): 
	angI=traduceElAnguloRelojATrigonometria(anguloIni)
	angF=traduceElAnguloRelojATrigonometria(anguloFin)
	drawArcColoured(draw,centroX,centroY,base,angF,angI,colorLine2)

# def dibujaArcoRelojColoreadoGrueso(draw,centroX,centroY,base,anguloIni,anguloFin,colorLine2,grosor):
	# angI=traduceElAnguloRelojATrigonometria(anguloIni)
	# angF=traduceElAnguloRelojATrigonometria(anguloFin)
	# drawArcColouredWithThickness(draw,centroX,centroY,base,angF,angI,colorLine2,grosor)

# def drawArcColouredWithThickness(draw, pxCentre, pyCentre, radio, AngIni, AngEnd,colorA,thickness):
	# arcx = dxf.arc(radio, (pxCentre,pyCentre), AngIni, AngEnd)
	# arcx['color'] = colorA
	# arcx['thickness'] = thickness
	# draw.add(arcx)
	# draw.add_layer(currentLayer, color=colorA)

def drawSolidTriangleFMC(draw, Ax, Ay, Bx, By, Cx, Cy,colorT):
	solid=dxf.solid([(Ax,Ay),(Bx,By),(Cx,Cy)])
	solid['color'] = colorT
	draw.add(solid)
	draw.add_layer(currentLayer, color=colorT)

def drawTriangleColoured(draw, Ax, Ay, Bx, By, Cx, Cy,colorT):
	oldx,oldy=drawLineColoured(draw,Ax,Ay,Bx,By,colorT)
	oldx,oldy=drawLineColoured(draw,Bx,By,Cx,Cy,colorT)
	oldx,oldy=drawLineColoured(draw,Cx,Cy,Ax, Ay,colorT)

def drawArcColoured(draw, pxCentre, pyCentre, radio, AngIni, AngEnd,colorA):
	arcx = dxf.arc(radio, (pxCentre,pyCentre), AngIni, AngEnd)
	arcx['color'] = colorA
	draw.add(arcx)
	draw.add_layer(currentLayer, color=colorA)

def drawArcColouredLayer(draw, pxCentre, pyCentre, radio, AngIni, AngEnd, colorA, capa):
	arcx = dxf.arc(radio, (pxCentre,pyCentre), AngIni, AngEnd)
	arcx['color'] = colorA
	arcx['layer'] = capa
	draw.add(arcx)
	draw.add_layer(capa, color=colorA)

def drawCircleColoured(draw,radio,pxCentre,pyCentre,colorA):
	circlex = dxf.circle(radio, (pxCentre,pyCentre))
	circlex['color']=colorA
	draw.add(circlex)

def drawCircleColouredLayer(draw,radio,pxCentre,pyCentre,colorA,capa):
	circlex = dxf.circle(radio, (pxCentre,pyCentre))
	circlex['color']=colorA
	circlex['layer'] = capa
	draw.add(circlex)
	draw.add_layer(capa, color=colorA)


def drawArcColouredAndThickness(draw, pxCentre, pyCentre, radio, AngIni, AngEnd,colorA,thicknes):
	#pre: thicknes float
	arcx = dxf.arc(radio, (pxCentre,pyCentre), AngIni, AngEnd)
	arcx['color'] = colorA
	arcx['thickness']=thicknes
	draw.add(arcx)
	draw.add_layer(currentLayer, color=colorA)

def drawArcFMC(draw, pxCentre, pyCentre, radio, AngIni, AngEnd):
	arcx = dxf.arc(radio, (pxCentre,pyCentre), AngIni, AngEnd)
	arcx['color'] = colorLine
	draw.add(arcx)
	draw.add_layer(currentLayer, color=colorLine)

def drawLineColoured(draw, pxOrig, pyOrig, pxDstn, pyDstn, colorL):
	linex = dxf.line((pxOrig, pyOrig), (pxDstn, pyDstn))
	linex['color'] = colorL
	draw.add(linex)
	draw.add_layer(currentLayer, color=colorL)
	return pxDstn,pyDstn

def drawLineColouredLayer(draw, pxOrig, pyOrig, pxDstn, pyDstn, colorL,capa):
	linex = dxf.line((pxOrig, pyOrig), (pxDstn, pyDstn))
	linex['color'] = colorL
	linex['layer'] = capa
	draw.add(linex)
	draw.add_layer(capa, color=colorL)
	return pxDstn,pyDstn

def writeTextNoAling(draw,txt,px0,py0,size,colorTextt,layerTxt,angRotation):
	text = dxf.text(txt, (px0,py0), height=size, rotation=angRotation)
	text['layer'] = layerTxt
	text['color'] = colorTextt
	#text['alignpoint']=alignPx,alignPy
	draw.add(text)

def writeTextAling(draw,txt,px0,py0,size,colorTextt,layerTxt):
	#text = dxf.text(txt, (px0,py0), height=size, rotation=angRotation)
	print(txt)
	text = dxf.mtext(txt,(px0,py0))
	text.layer = layerTxt
	text.color = colorTextt
	text.height = size
##	text['layer'] = layerTxt
##	text['color'] = colorTextt
	#text['alignpoint']=alignPx,alignPy
	#text['alignpoint']=px0,py0
	draw.add(text)
	

def writeTextLeft(draw,txt,px0,py0,size,colorTextt,layerTxt,angRotation):
	text = dxf.text(txt, (px0,py0), height=size, rotation=angRotation)
	text['layer'] = layerTxt
	text['color'] = colorTextt
	#text['alignpoint']=alignPx,alignPy
	draw.add(text)

def writeTextRight(draw,txt,alignpx,alignpy,size,colorTextt,layerTxt,angRotation):
	text=dxf.text(txt, halign=RIGHT, alignpoint=(alignpx,alignpy))
	text['layer'] = layerTxt
	text['color'] = colorTextt
	text['height']= size
	draw.add(text)

def writeText(draw,txt,alignpx,alignpy,size,colorTextt,layerTxt,angRotation):
	text=dxf.text(txt, halign=CENTER, alignpoint=(alignpx,alignpy))
	text['layer'] = layerTxt
	text['color'] = colorTextt
	text['height']= size
	draw.add(text)
'''
def damePuntocentral(txt,px0,py0,tamfte):
	#pre: txt no vacio al menos una letra, tamfte entre 6 y 36
        #post: devuelve el inicio la posicion para que quede centrado
	numLetras=len(txt)
	if tamfte < 6:
		ratio=7
	elif tamfte ==6:
		ratio=8
	elif tamfte ==7:
		ratio=9
	elif tamfte ==7.5:
		ratio=10
	elif tamfte ==8:
		ratio=11
	elif tamfte ==9:
		ratio=12
	elif tamfte ==10:
		ratio=13
	elif tamfte ==10.5:
		ratio=14
	elif tamfte ==11:
		ratio=15
	elif tamfte ==12:
		ratio=16
	elif tamfte ==13:
		ratio=17
	elif tamfte ==13.5:
		ratio=18
	elif tamfte ==14:
		ratio=19
	elif tamfte ==14.5:
		ratio=20
	elif tamfte ==15:
		ratio=21
	elif tamfte ==16:
		ratio=22
	elif tamfte ==17:
		ratio=23
	elif tamfte ==18:
		ratio=24
	elif tamfte ==19:
		ratio=25
	elif tamfte ==20:
		ratio=26
	elif tamfte ==21:
		ratio=27
	elif tamfte ==22:
		ratio=29
	elif tamfte ==23:
		ratio=30
	elif tamfte ==24:
		ratio=32
	elif tamfte ==25:
		ratio=33
	elif tamfte ==26:
		ratio=35
	elif tamfte ==27:
		ratio=36
	elif tamfte ==28:
		ratio=37
	elif tamfte ==29:
		ratio=38
	elif tamfte ==30:
		ratio=40
	elif tamfte ==31:
		ratio=41
	elif tamfte ==32:
		ratio=42
	elif tamfte ==33:
		ratio=43
	elif tamfte ==34:
		ratio=45
	elif tamfte ==35:
		ratio=46
	elif tamfte ==36:
		ratio=48
	else:
		ratio=49
	espacio=numLetras * ratio /2
	print ("el espacio es:" + espacio + "|")
	return (px0 - espacio),py0
'''


def drawCircle(draw, cx, cy ,radius):
#pre: draw=dxf.drawing('filename.dxf'), radius > 0
#post: it draws a circle
#return point top Right of external square (out of the form)
	drawArcFMC(draw, cx, cy, radius,0, 0)
	cx +=radius
	cy +=radius
	return cx,cy

def creaTroncoConoCapaConDesplazamiento(drawing,anguloIni,anguloFin,base,altura,centroX,centroY,colorLine3,capa):
#prev: drawing un dxf.drawing valido
#post: dibuja un tronco cono con centro en centroX y centroY y devuelve sus puntos extremos
#		px0,py0 es el punto inferior del angulo inicial
#		pxd,pyd es el punto inferior del angulo final
#		px0a,py0a es el punto superior del angulo inicial
#		pxda,pyda es el punto superior del angulo inicial
	dibujaArcoRelojColoreadoCapa(drawing,centroX,centroY,base,anguloIni,anguloFin,colorLine3,capa)
	dibujaArcoRelojColoreadoCapa(drawing,centroX,centroY,altura,anguloIni,anguloFin,colorLine3,capa)
	px0,py0 = damePtoArcoReloj(centroX,centroY,anguloIni,base)
	pxd,pyd = damePtoArcoReloj(centroX,centroY,anguloFin,base)
	px0a,py0a = damePtoArcoReloj(centroX,centroY,anguloIni,altura)
	pxda,pyda = damePtoArcoReloj(centroX,centroY,anguloFin,altura)
	drawLineColouredLayer(drawing, px0, py0, px0a,  py0a, colorLine3,capa)
	drawLineColouredLayer(drawing, pxd, pyd, pxda,  pyda, colorLine3,capa)
	drawing.save()
	return px0,py0,pxd,pyd,px0a,py0a,pxda,pyda

def creaTroncoConoCapa(drawing,anguloIni,anguloFin,base,altura,colorLine3,capa):
#prev: drawing un dxf.drawing valido
#post: dibuja un tronco cono y devuelve sus puntos extremos
#		px0,py0 es el punto inferior del angulo inicial
#		pxd,pyd es el punto inferior del angulo final
#		px0a,py0a es el punto superior del angulo inicial
#		pxda,pyda es el punto superior del anngulo inicial
	dibujaArcoRelojColoreadoCapa(drawing,centroX,centroY,base,anguloIni,anguloFin,colorLine3,capa)
	dibujaArcoRelojColoreadoCapa(drawing,centroX,centroY,altura,anguloIni,anguloFin,colorLine3,capa)
	px0,py0 = damePtoArcoReloj(centroX,centroY,anguloIni,base)
	pxd,pyd = damePtoArcoReloj(centroX,centroY,anguloFin,base)
	px0a,py0a = damePtoArcoReloj(centroX,centroY,anguloIni,altura)
	pxda,pyda = damePtoArcoReloj(centroX,centroY,anguloFin,altura)
	drawLineColouredLayer(drawing, px0, py0, px0a,  py0a, colorLine3,capa)
	drawLineColouredLayer(drawing, pxd, pyd, pxda,  pyda, colorLine3,capa)
	drawing.save()
	return px0,py0,pxd,pyd,px0a,py0a,pxda,pyda

def creaTroncoCono(drawing,anguloIni,anguloFin,base,altura,colorLine3):
	dibujaArcoRelojColoreado(drawing,centroX,centroY,base,anguloIni,anguloFin,colorLine3)
	dibujaArcoRelojColoreado(drawing,centroX,centroY,altura,anguloIni,anguloFin,colorLine3)
	px0,py0 = damePtoArcoReloj(centroX,centroY,anguloIni,base)
	pxd,pyd = damePtoArcoReloj(centroX,centroY,anguloFin,base)
	px0a,py0a = damePtoArcoReloj(centroX,centroY,anguloIni,altura)
	pxda,pyda = damePtoArcoReloj(centroX,centroY,anguloFin,altura)
	drawLineColoured(drawing, px0, py0, px0a,  py0a, colorLine3)
	drawLineColoured(drawing, pxd, pyd, pxda,  pyda, colorLine3)
	drawing.save()
	return px0,py0,pxd,pyd,px0a,py0a,pxda,pyda

def creaTroncoConoSolidoCapa(drawing,anguloIni,anguloFin,base,altura,colorLine3,capa):
	px0,py0,pxd,pyd,px0a,py0a,pxda,pyda=creaTroncoConoCapa(drawing,anguloIni,anguloFin,base,altura,colorLine3,capa)
	for i in range(base, altura):
		dibujaArcoRelojColoreadoCapa(drawing,centroX,centroY,i,anguloIni,anguloFin,colorLine3,capa)
		k=0
		for j in range(0, 8):
			k=k+0.1
			dibujaArcoRelojColoreadoCapa(drawing,centroX,centroY,i+k,anguloIni,anguloFin,colorLine3,capa)
		drawing.save()
	return px0,py0,pxd,pyd,px0a,py0a,pxda,pyda
    
def creaPorcentajeCirculos(drawing,posIniX,posIniY,vector,espacio,capaNumeros):
    #pre: vector es un diccionario con nombre y porcentaje de habilidad
    #     porcentaje <=100
    #post: muestra los valores de vector en el centro de cada aro
    #       pintando 5 colores
##        writeTextNoAling(drawing,txt,px0,py0,size,colorTextt,layerTxt,angRotation)
        listaKeys=[]
        listaValues=[]
        listaKeys.extend(vector.keys())
        listaValues.extend(vector.values())
        numCirculos=len(vector)
        pxDstn=posIniX
        pyDstn=posIniY
        for i in range (1, numCirculos):
                txt=str (listaValues[i])+" %"
                #writeTextNoAling(drawing,txt,pxDstn,pyDstn,8,0,capaNumeros,0)
                writeTextNoAling(drawing,txt,pxDstn,pyDstn,8,0,capaNumeros,0)
                pxDstn=pxDstn+espacio

def creaTituloCirculos(drawing,posIniX,posIniY,vector,espacio,desplazamientoVertical,capaNumeros):
   #pre: vector es un diccionario con nombre como key y porcentaje de habilidad como value
    #post: muestra las keys del diccionario vector en bajo cada aro
        listaKeys=[]
        listaValues=[]
        listaKeys.extend(vector.keys())
#        listaValues.extend(vector.values())
        pxDstn=posIniX
        numCirculos=len(vector)
        pyDstn=posIniY - desplazamientoVertical
        for i in range (1, numCirculos):
                txt=str (listaKeys[i])
                #writeTextNoAling(drawing,txt,pxDstn,pyDstn,8,0,capaNumeros,0)
                writeTextNoAling(drawing,txt,pxDstn,pyDstn,8,0,capaNumeros,0)
                pxDstn=pxDstn+espacio

def muestraCirculosHabilidades(drawing,radio,anchoAro,posIniX,posIniY,vector,espacio,capaBase,capaColor,capaNumeros,capaTitulo):
    #pre: vector es un diccionario con nombre y porcentaje de habilidad
    #    anchoAro la distancia entre elcirculo exterior y el interior, porcentaje <=100
    #post: dibuja tantos aros como claves hay en vector y completados segun los valores de vector
    #       pintando 5 colores
        creaCirculosBaseHabilidadesVector(drawing,radio,anchoAro,posIniX,posIniY,vector,espacio,capaBase)
        creaCirculosColorHabilidadesVector(drawing,radio,anchoAro,posIniX,posIniY,vector,espacio,capaColor)
        creaPorcentajeCirculos(drawing,posIniX,posIniY,vector,espacio,capaNumeros)
        creaTituloCirculos(drawing,posIniX,posIniY,vector,espacio,radio +(anchoAro * 2),capaTitulo)
##	creaCirculosColorHabilidadesVector(drawing,radio,anchoAro,PosIniX,PosIniY,vector,espacio,capaColor)
    
def creaCirculosBaseHabilidades(drawing,radio,anchoAro,posIniX,posIniY,numCirculos,espacio,capa):
##        numCirculos=len(vector)
        pxDstn=posIniX
        pyDstn=posIniY
        for i in range (1, numCirculos):
                #pxDstn,pyDstn=drawCircleColouredLayer(drawing,radio,pxDstn,pyDstn,0,capa)
                creaAro(drawing,radio,anchoAro,pxDstn,pyDstn,0,100,capa)
                pxDstn=pxDstn+espacio
        return pxDstn,pyDstn

def creaCirculosBaseHabilidadesVector(drawing,radio,anchoAro,posIniX,posIniY,vector,espacio,capa):
        numCirculos=len(vector)
        pxDstn=posIniX
        pyDstn=posIniY
        for i in range (1, numCirculos):
                #pxDstn,pyDstn=drawCircleColouredLayer(drawing,radio,pxDstn,pyDstn,0,capa)
                creaAro(drawing,radio,anchoAro,pxDstn,pyDstn,0,100,capa)
                pxDstn=pxDstn+espacio
        return pxDstn,pyDstn


def creaCirculosColorHabilidadesVector(drawing,radio,anchoAro,posIniX,posIniY,vector,espacio,capa):
    #pre: vector es un diccionario con nombre y porcentaje de habilidad
    #post: dibuja tantos aros como claves hay en vector y completados segun los valores de vector
    #       pintando 5 colores
        listaKeys=[]
        listaValues=[]
        listaKeys.extend(vector.keys())
        listaValues.extend(vector.values())
        numCirculos=len(vector)
        pxDstn=posIniX
        pyDstn=posIniY
        for i in range (1, numCirculos):
                #pxDstn,pyDstn=drawCircleColouredLayer(drawing,radio,pxDstn,pyDstn,0,capa)
                creaAro(drawing,radio,anchoAro,pxDstn,pyDstn,(i%5)+1,vector[listaKeys[i]],capa)
                pxDstn=pxDstn+espacio
        return pxDstn,pyDstn
    
def creaAro(drawing,radioExt,anchoAro,posIniX,posIniY,color,porcentaje,capa):
    #pre: anchoAro distantia entre elcirculo exterior y el interior, porcentaje <=100
    #post: dibuja dos circulos concentricos si porcentaje < 100 no se completa el aro
        if (porcentaje==100):
                drawCircleColouredLayer(drawing,radioExt,posIniX,posIniY,color,capa)
                drawCircleColouredLayer(drawing,radioExt - anchoAro,posIniX,posIniY,color,capa)
        else:
                creaTroncoConoCapaConDesplazamiento(drawing,0,traducePorcentajeAAngulo(porcentaje),radioExt - anchoAro,radioExt,posIniX,posIniY,color,capa)
                #creaTroncoConoCapa(drawing,anguloIni,anguloFin,base,altura,colorLine3,capa):
            
def traducePorcentajeAAngulo(porcentaje):
        ang=(360*porcentaje)/100
        return ang
    
def main():
	anguloIni=0.0
	anguloFin=359.9
	base=40
	altura=55
	anguloIni1=60
	anguloFin1=100
	altura1=60
	altura2=70
	primeraLinea=5
	segundaLinea=10
	espacio=100
	drawing = dxf.drawing('habilidades.dxf')
	vector={'.Net':55,'Photoshop':50,'Pinnacle':50,'Illustrator':55,'Php':70,'Css':60,'MySql':50,'Dreamweaver':80,'Java':70,'Android':50} 
        #set value
##	drawCircleColouredLayer(drawing,55,320,20,colorLine5,'sector1')
	Px=20
	Py=20
##	creaCirculosBaseHabilidades(drawing,40,9,Px,Py,vector,espacio,'base')
##	creaCirculosColorHabilidadesVector(drawing,40,9,Px,Py,vector,espacio,'circulos')
##def testeaAlineacionLetras(draw,angIni,angFin,xCenter,yCenter,radio,color,capa):
	#testeaAlineacionLetras(drawing,0,0,200,200,40,0,'numeros')
	#print (Px)
##	escribeEnArcoCapa(drawing,"hola",200,200,0,0,0,0,8,'numeros')
	#Px,Py=damePuntocentral("hola",20,5,8)
	#print (Px)
	#def writeTextAling(draw,txt,px0,py0,size,colorTextt,layerTxt,tamFte):
	#writeTextAling(drawing,"hola",200,200,8,0,'numeros')
##	writeText(drawing,"hola",20,5,8,0,'numeros',0)
##	writeTextNoAling(drawing,"",40,5,8,0,'numeros',0)
##	writeText(drawing,"adios",40,5,8,0,'numeros',0)
	muestraCirculosHabilidades(drawing,40,9,Px,Py,vector,espacio,'base','circulos','numeros','aplicacion')
##	muestraCirculosHabilidades(drawing,radio,anchoAro,posIniX,posIniY,vector,espacio,capaBase,capaColor,capaNumeros)
	##	def creaCirculosColorHabilidadesVector(drawing,vector,radio,anchoAro,posIniX,posIniY,numCirculos,espacio,capa):

	#escribeEnArco(drawing,'universidad',centroX,centroY,base,anguloIni,anguloFin,colorLine,5)
	drawing.save()
	#-----------------------------------------------------------------
	# msize, nsize = (altura-base,altura-base)

	# mesh = dxf.polymesh(msize, nsize)
	# delta = math.pi / msize
	# for x in range(msize):
		# sinx = math.sin(float(x)*delta)
		# for y in range(nsize):
			# cosy = math.cos(float(y)*delta)
			# z = sinx * cosy * 3.0
			# mesh.set_vertex(x, y, (x,y,z))
	# drawing.add(mesh)
	#----------------------------
	# solid = dxf.solid([(px0,py0), (pxd,pyd),  (pxda,pyda) ,(px0a,py0a)], color=2)
	# solid['layer'] = 'solids'
	# solid['color'] = 7
	# drawing.add(solid)
	# drawing.save()
	#------------------------------------
	# solid = dxf.solid([(px0,py0), (pxd,pyd), (px0a,py0a)], color=1)
	# solid['layer'] = 'solids'
	# solid['color'] = 7
	# drawing.add(solid)
#	drawing.add_layer(currentLayer, color=colorT)
#-------------------------
	# polyline= dxf.polyline(linetype='CONTINUOUS')
	# polyline.add_vertices( [(px0,py0), (pxd,pyd),  (pxda,pyda) ,(px0a,py0a),(px0,py0)] )
	# drawing.add(polyline)
	# drawing.save()
#-------------------------



if __name__ == '__main__' : main()
