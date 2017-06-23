/* Sydney Strzempko (c) for New American Public Art Color Commons project
 * Loader functions for sunburst graphic, linked to DATAVIZ.HTML
 * Instantiates with main() call from body ONLOAD method, fed python list of dicts
 */

function main(data)
{
    load_burst(data,closure) // Calls with assumption of asynchronous updating   
    load_info() // Executes unrelated to burst display
}

function load_burst(data,closure)
{
    //uses large amount of D3 and sunburst optmz
    // ACCESSESS CANVAS ID IN BODY
    return closure()
}

function load_info(tab)
{
    //jquery or whatever to explain what is needed
    //eg, the dynamic element
    // ACCESSES INFO class in body
}

function update_burst(data)
{

}

function showtabs(i)
{
    arr = document.getElementsByClassName('tabs')
    if (i==2){

    } else if (i==1) {

    } else { //i==0
	
    }
    for (j=0;j<3;j++){
	if (j!=i){
	    arr[j][0]
	}
    }	
}
