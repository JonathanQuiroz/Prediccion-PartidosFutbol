import numpy as np
from IPython.display import Markdown,display

# Funcion que trae registro de el equipo deseado
def consultaEquipo(equipo):

	# Organizamos formato de equipo ingresado
	equipo = format(equipo.encode("utf-8"))
	regTabla = []

	# Leemos archivo de texto con datos de los equipos
	reg = np.loadtxt("datos.md", dtype=str, delimiter="\n")

	try:

		# Recorremos registros buscando datos de equipo y descartamos 
		# registros repetidos
		for i in range(2,len(reg)):
			for j in range(2,len(reg)):
				if equipo in reg[i] or equipo in reg[i]:
					if reg[i] != reg[j]:
						regTabla += [i]

		# Convertimos la lista de registros en string para mostrarla
		# en markdown
		visTabla = "\n".join(reg[regTabla[0]:regTabla[-1]])

		# Mostramos tabla
		display(Markdown(reg[0]+"\n"+reg[1]+"\n"+visTabla))

	except IndexError:
		# Si no se encuentran datos del equipo sacamos este mensaje
		print "No hay datos para mostrar de este equipo"

	
	
