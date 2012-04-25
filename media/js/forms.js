

function popup(url){
	window.open(url,"janela1","width=600,height=300,scrollbars=YES")
} 

function validaFinalizarMapa(){
	var empresa=document.forms["form"]["for"].value;
	var opcao=confirm("Confirmar cotação da empresa "+empresa+" como vencedora?");
	if (opcao==false){
		return false;
	}else{
		
	}
}
