

function show_confirm(){
	var r=confirm("Confirmar o envio");
	if (r==false){
		return false;
	}else{
	
	}
}

function validaFinalizarMapa(){
	var empresa=document.forms["form"]["for"].value;
	var opcao=confirm("Confirmar cotação da empresa "+empresa+" como vencedora?");
	if (opcao==false){
		return false;
	}else{
		
	}
}
