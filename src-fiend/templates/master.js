/* Sydney Strzempko (c) for New American Public Art Color Commons project
 * Loader functions for sunburst graphic, linked to DATAVIZ.HTML
 * Instantiates with main() call from window ONLOAD method, fed python list of dicts
 * Strongly modified from https://bl.ocks.org/denjn5/1a3f8e44cdcb3054121dfd991f59fbc2
 * With additional mods from https://bl.ocks.org/maybelinot/5552606564ef37b5de7e47ed2b7dc099 */

// INSTANTIATOR - collects and validates data-attribute info fr embedded index.html
window.onload = function() {
    var log = d3.select("#canvas").attr("data-log");
    var cur = d3.select("#about").attr("data-time");
    var all = parseInt(d3.select(".tabs").attr("data-all"));
    main(log,cur,all);
};

// MAIN - coordinates CANVAS data viz (using data/log) and TIME update
function main(data,time,all) {
    load_about(time); // Coordinates 2/2 page
    tree = traverse_tree(data, JSON.parse);
    load_data(tree,all); // Calls with assumption of asynchronous updating? TODO 1/2
}

// DATA VIZ MAIN - coordinates canvas drawing
function load_data(data,all) {
    var WID = 600, HEI = 600, RAD = (Math.min(WID,HEI)/2)-10,
	//gscale = d3.scaleSequential(d3.interpolateGreys),
    partition = d3.partition()
	  .size([2*Math.PI, RAD]),
	root = d3.hierarchy(data)
	  .sum(function(d) { return d.size; })
	  .sort(function(a,b) { return b.value - a.value; }),
	g = d3.select("svg")
	  .append("g")
	  .attr("transform","translate("+WID/2+","+(HEI/2)+")"),
	node = root,
	arc = d3.arc()
	  .startAngle(function(d) { d.x0s = d.x0; return d.x0; }) //set start angles
	  .endAngle(function(d) { d.x1s = d.x1; return d.x1; })
	  .innerRadius(function(d) { return d.y0; })
	  .outerRadius(function(d) { return d.y1; });

    partition(root); //calls partition on root (links structure & data)
    load_tabs(root,all);
	
    var run = function(root) { 		
        partition(root); //calls partition on root (links structure & data)

        console.log("populating dataset from:");
        console.log(root);

		var slice = g.selectAll('g') //does this grab all? TODO
		  .data(root.descendants())
		  .enter()
		  .append('g')
            .attr("class", function (d) { return rowize(d); });

    	slice.append('path')
		    .attr("display", function (d) { return d.depth ? null : "none"; })
		    .attr("d", arc)
			.style('stroke', '#000066')
			.style("fill", function (d) { return colorize(d); });
 
        // TODO - gscale pscale syntax
  		var gscale = d3.scaleSequential(d3.interpolateGreys)
                    .domain([0,24]);
        //            .interpolator(d3.interpolateGreys);
        var pscale = d3.scaleSequential(d3.interpolateYlGnBu)
                    .domain([0,500]);

        // TODO - needs to be fixed/modified
        g.selectAll('.hr')
            .style("fill", function (d) { return gscale(d) });
	    g.selectAll('.person')
            .style("fill", function (d) { return pscale(d) });

        // Set hover elements for tooltip; can be accessed with viewport funct
		g.selectAll('.node')
          .on("mouseover", function (d,i) { showtext(d); })
          .on("mouseout", function (d,i) { killtext(d); })
          .on("click", function(d,i) { zoom(d);})
          .append("title")
		    .text(function(d) { return d.data.size? d.data.msg : d.data.name; });



    }
    run(root);
}

// HELPER FUNCTIONS //

//TODO - smooth sorting tweening

//zoom: zooms to new node as partition center
function zoom(node) {
    run(node);
}

//rwoise: SORTS LEVELS w unique class marker
function rowize(node) {
    var row = "";
    if (!node.data.msg){
        var str = node.data.name;
        if (str.slice(0,2) == "hr") {
            row = " hr";
        } else {
            var len = str.length;//8, we want index *4|5|6|7, so 8-(4) = 4
            if ((str.charAt(len-4) == '-') || (str.charAt(len-3) == '-')) { // a NAME eg, Ms. MARY-123 OR trailing 0 Ms. HAM-78
                row = " person";
            } else if (str.charAt(3) == ' '){// So now check for TUE[]23rd
                row = " day";
            } else {            // Would be... months, yr, etc
                row = " other";
            }
        }
    } //else; leafs need no other class
    return "node"+row;
}

// colorize: FINDS COLOR for each slice based on node
function colorize(node) {
    var lookup = "black";
    if (node.data.msg) {
        lookup = COLORS[node.data['msg'].toLowerCase()];   
        if (lookup == null) {
	       lookup = "white";//color scale - our space/dom
        }
    }
    return d3.color(lookup);
}

// showtext: TOGGLES TEXT over slices of data viz, pulls fr title
function showtext(d) {
	var title = d.data.size? d.data.msg : d.data.name; 
    d3.selectAll('.tabs')
      .select('#view')
        .html("<b>NODE:</b> "+title+" ");
}

//killtext: TOGGLES nontext over nonslice
function killtext(d) {
    d3.selectAll('.tabs')
      .select('#view')
        .html("<b>NODE:</b> --- ");
}
	
// load_tabs: DISPLAYS relevant tab component when selected
function load_tabs(tree,num) {
    var format = [("<b>Total Texts for All Time:</b> "+num),
                ("<b>Total Texts for "+tree.data.name+":</b> "+tree.value)];
    d3.select('.tabs')
        .insert('div')
            .attr('id','view')
            .html('<b>NODE:</b> ___ ');
    d3.select('.tabs')           
        .insert('div')
            .attr('id','aspan')
            .html(format[0]);
    d3.select('.tabs')
        .insert('div')
            .attr('id','tspan')
            .html(format[1]);
}

// load_about: LOADER for ABOUT - provides last-updated information
function load_about(time) {
    var val = new Date(parseInt(time));
    var format = "Last Updated: " + val + ".";
    d3.select("#about").insert("div",":first-child").html(format);
}
	
// traverse_tree: CONVERTS raw string=>nested JSON dict format
function traverse_tree(raw, apply) {
    if (typeof raw === 'string'){ //parse it regardless, then assess children/recall	
    	raw = apply(raw);
	raw = traverse_tree(raw,apply);
    } else if (Array.isArray(raw)) {
	raw.forEach(function(val, i){ raw[i] = traverse_tree(val,apply); });
    }
    return raw;
}

// GLOBAL VARS
COLORS = {'acid green':'#8ffe09','adobe':'#bd6c48','algae':'#54ac68','algae green':'#21c36f','almost black':'#070d0d','amber':'#feb308','amethyst':'#9b5fc0','apple':'#6ecb3c','apple green':'#76cd26','apricot':'#ffb16d','aqua':'#13eac9','aqua blue':'#02d8e9','aqua green':'#12e193','aqua marine':'#2ee8bb','aquamarine':'#04d8b2','army green':'#4b5d16','asparagus':'#77ab56','aubergine':'#3d0734','auburn':'#9a3001','avocado':'#90b134','avocado green':'#87a922','azul':'#1d5dec','azure':'#069af3','baby blue':'#a2cffe','baby green':'#8cff9e','baby pink':'#ffb7ce','baby poo':'#ab9004','baby poop':'#937c00','baby poop green':'#8f9805','baby puke green':'#b6c406','baby purple':'#ca9bf7','baby shit brown':'#ad900d','baby shit green':'#889717','banana':'#ffff7e','banana yellow':'#fafe4b','barbie pink':'#fe46a5','barf green':'#94ac02','barney':'#ac1db8','barney purple':'#a00498','battleship grey':'#6b7c85','beige':'#e6daa6','berry':'#990f4b','bile':'#b5c306','black':'#000000','bland':'#afa88b','blood':'#770001','blood orange':'#fe4b03','blood red':'#980002','blue':'#0343df','blue blue':'#2242c7','blue green':'#137e6d','blue grey':'#607c8e','blue purple':'#5729ce','blue violet':'#5d06e9','blue with a hint of purple':'#533cc6','blue/green':'#0f9b8e','blue/grey':'#758da3','blue/purple':'#5a06ef','blueberry':'#464196','bluegreen':'#017a79','bluegrey':'#85a3b2','bluey green':'#2bb179','bluey grey':'#89a0b0','bluey purple':'#6241c7','bluish':'#2976bb','bluish green':'#10a674','bluish grey':'#748b97','bluish purple':'#703be7','blurple':'#5539cc','blush':'#f29e8e','blush pink':'#fe828c','booger':'#9bb53c','booger green':'#96b403','bordeaux':'#7b002c','boring green':'#63b365','bottle green':'#044a05','brick':'#a03623','brick orange':'#c14a09','brick red':'#8f1402','bright aqua':'#0bf9ea','bright blue':'#0165fc','bright cyan':'#41fdfe','bright green':'#01ff07','bright lavender':'#c760ff','bright light blue':'#26f7fd','bright light green':'#2dfe54','bright lilac':'#c95efb','bright lime':'#87fd05','bright lime green':'#65fe08','bright magenta':'#ff08e8','bright olive':'#9cbb04','bright orange':'#ff5b00','bright pink':'#fe01b1','bright purple':'#be03fd','bright red':'#ff000d','bright sea green':'#05ffa6','bright sky blue':'#02ccfe','bright teal':'#01f9c6','bright turquoise':'#0ffef9','bright violet':'#ad0afd','bright yellow':'#fffd01','bright yellow green':'#9dff00','british racing green':'#05480d','bronze':'#a87900','brown':'#653700','brown green':'#706c11','brown grey':'#8d8468','brown orange':'#b96902','brown red':'#922b05','brown yellow':'#b29705','brownish':'#9c6d57','brownish green':'#6a6e09','brownish grey':'#86775f','brownish orange':'#cb7723','brownish pink':'#c27e79','brownish purple':'#76424e','brownish red':'#9e3623','brownish yellow':'#c9b003','browny green':'#6f6c0a','browny orange':'#ca6b02','bruise':'#7e4071','bubble gum pink':'#ff69af','bubblegum':'#ff6cb5','bubblegum pink':'#fe83cc','buff':'#fef69e','burgundy':'#610023','burnt orange':'#c04e01','burnt red':'#9f2305','burnt siena':'#b75203','burnt sienna':'#b04e0f','burnt umber':'#a0450e','burnt yellow':'#d5ab09','burple':'#6832e3','butter':'#ffff81','butter yellow':'#fffd74','butterscotch':'#fdb147','cadet blue':'#4e7496','camel':'#c69f59','camo':'#7f8f4e','camo green':'#526525','camouflage green':'#4b6113','canary':'#fdff63','canary yellow':'#fffe40','candy pink':'#ff63e9','caramel':'#af6f09','carmine':'#9d0216','carnation':'#fd798f','carnation pink':'#ff7fa7','carolina blue':'#8ab8fe','celadon':'#befdb7','celery':'#c1fd95','cement':'#a5a391','cerise':'#de0c62','cerulean':'#0485d1','cerulean blue':'#056eee','charcoal':'#343837','charcoal grey':'#3c4142','chartreuse':'#c1f80a','cherry':'#cf0234','cherry red':'#f7022a','chestnut':'#742802','chocolate':'#3d1c02','chocolate brown':'#411900','cinnamon':'#ac4f06','claret':'#680018','clay':'#b66a50','clay brown':'#b2713d','clear blue':'#247afd','cloudy blue':'#acc2d9','cobalt':'#1e488f','cobalt blue':'#030aa7','cocoa':'#875f42','coffee':'#a6814c','cool blue':'#4984b8','cool green':'#33b864','cool grey':'#95a3a6','copper':'#b66325','coral':'#fc5a50','coral pink':'#ff6163','cornflower':'#6a79f7','cornflower blue':'#5170d7','cranberry':'#9e003a','cream':'#ffffc2','creme':'#ffffb6','crimson':'#8c000f','custard':'#fffd78','cyan':'#00ffff','dandelion':'#fedf08','dark':'#1b2431','dark aqua':'#05696b','dark aquamarine':'#017371','dark beige':'#ac9362','dark blue':'#00035b','dark blue green':'#005249','dark blue grey':'#1f3b4d','dark brown':'#341c02','dark coral':'#cf524e','dark cream':'#fff39a','dark cyan':'#0a888a','dark forest green':'#002d04','dark fuchsia':'#9d0759','dark gold':'#b59410','dark grass green':'#388004','dark green':'#033500','dark green blue':'#1f6357','dark grey':'#363737','dark grey blue':'#29465b','dark hot pink':'#d90166','dark indigo':'#1f0954','dark khaki':'#9b8f55','dark lavender':'#856798','dark lilac':'#9c6da5','dark lime':'#84b701','dark lime green':'#7ebd01','dark magenta':'#960056','dark maroon':'#3c0008','dark mauve':'#874c62','dark mint':'#48c072','dark mint green':'#20c073','dark mustard':'#a88905','dark navy':'#000435','dark navy blue':'#00022e','dark olive':'#373e02','dark olive green':'#3c4d03','dark orange':'#c65102','dark pastel green':'#56ae57','dark peach':'#de7e5d','dark periwinkle':'#665fd1','dark pink':'#cb416b','dark plum':'#3f012c','dark purple':'#35063e','dark red':'#840000','dark rose':'#b5485d','dark royal blue':'#02066f','dark sage':'#598556','dark salmon':'#c85a53','dark sand':'#a88f59','dark sea green':'#11875d','dark seafoam':'#1fb57a','dark seafoam green':'#3eaf76','dark sky blue':'#448ee4','dark slate blue':'#214761','dark tan':'#af884a','dark taupe':'#7f684e','dark teal':'#014d4e','dark turquoise':'#045c5a','dark violet':'#34013f','dark yellow':'#d5b60a','dark yellow green':'#728f02','darkblue':'#030764','darkgreen':'#054907','darkish blue':'#014182','darkish green':'#287c37','darkish pink':'#da467d','darkish purple':'#751973','darkish red':'#a90308','deep aqua':'#08787f','deep blue':'#040273','deep brown':'#410200','deep green':'#02590f','deep lavender':'#8d5eb7','deep lilac':'#966ebd','deep magenta':'#a0025c','deep orange':'#dc4d01','deep pink':'#cb0162','deep purple':'#36013f','deep red':'#9a0200','deep rose':'#c74767','deep sea blue':'#015482','deep sky blue':'#0d75f8','deep teal':'#00555a','deep turquoise':'#017374','deep violet':'#490648','denim':'#3b638c','denim blue':'#3b5b92','desert':'#ccad60','diarrhea':'#9f8303','dirt':'#8a6e45','dirt brown':'#836539','dirty blue':'#3f829d','dirty green':'#667e2c','dirty orange':'#c87606','dirty pink':'#ca7b80','dirty purple':'#734a65','dirty yellow':'#cdc50a','dodger blue':'#3e82fc','drab':'#828344','drab green':'#749551','dried blood':'#4b0101','duck egg blue':'#c3fbf4','dull blue':'#49759c','dull brown':'#876e4b','dull green':'#74a662','dull orange':'#d8863b','dull pink':'#d5869d','dull purple':'#84597e','dull red':'#bb3f3f','dull teal':'#5f9e8f','dull yellow':'#eedc5b','dusk':'#4e5481','dusk blue':'#26538d','dusky blue':'#475f94','dusky pink':'#cc7a8b','dusky purple':'#895b7b','dusky rose':'#ba6873','dust':'#b2996e','dusty blue':'#5a86ad','dusty green':'#76a973','dusty lavender':'#ac86a8','dusty orange':'#f0833a','dusty pink':'#d58a94','dusty purple':'#825f87','dusty red':'#b9484e','dusty rose':'#c0737a','dusty teal':'#4c9085','earth':'#a2653e','easter green':'#8cfd7e','easter purple':'#c071fe','ecru':'#feffca','egg shell':'#fffcc4','eggplant':'#380835','eggplant purple':'#430541','eggshell':'#ffffd4','eggshell blue':'#c4fff7','electric blue':'#0652ff','electric green':'#21fc0d','electric lime':'#a8ff04','electric pink':'#ff0490','electric purple':'#aa23ff','emerald':'#01a049','emerald green':'#028f1e','evergreen':'#05472a','faded blue':'#658cbb','faded green':'#7bb274','faded orange':'#f0944d','faded pink':'#de9dac','faded purple':'#916e99','faded red':'#d3494e','faded yellow':'#feff7f','fawn':'#cfaf7b','fern':'#63a950','fern green':'#548d44','fire engine red':'#fe0002','flat blue':'#3c73a8','flat green':'#699d4c','fluorescent green':'#08ff08','fluro green':'#0aff02','foam green':'#90fda9','forest':'#0b5509','forest green':'#06470c','forrest green':'#154406','french blue':'#436bad','fresh green':'#69d84f','frog green':'#58bc08','fuchsia':'#ed0dd9','gold':'#dbb40c','golden':'#f5bf03','golden brown':'#b27a01','golden rod':'#f9bc08','golden yellow':'#fec615','goldenrod':'#fac205','grape':'#6c3461','grape purple':'#5d1451','grapefruit':'#fd5956','grass':'#5cac2d','grass green':'#3f9b0b','grassy green':'#419c03','green':'#15b01a','green apple':'#5edc1f','green blue':'#06b48b','green brown':'#544e03','green grey':'#77926f','green teal':'#0cb577','green yellow':'#c9ff27','green/blue':'#01c08d','green/yellow':'#b5ce08','greenblue':'#23c48b','greenish':'#40a368','greenish beige':'#c9d179','greenish blue':'#0b8b87','greenish brown':'#696112','greenish cyan':'#2afeb7','greenish grey':'#96ae8d','greenish tan':'#bccb7a','greenish teal':'#32bf84','greenish turquoise':'#00fbb0','greenish yellow':'#cdfd02','greeny blue':'#42b395','greeny brown':'#696006','greeny grey':'#7ea07a','greeny yellow':'#c6f808','grey':'#929591','grey blue':'#6b8ba4','grey brown':'#7f7053','grey green':'#789b73','grey pink':'#c3909b','grey purple':'#826d8c','grey teal':'#5e9b8a','grey/blue':'#647d8e','grey/green':'#86a17d','greyblue':'#77a1b5','greyish':'#a8a495','greyish blue':'#5e819d','greyish brown':'#7a6a4f','greyish green':'#82a67d','greyish pink':'#c88d94','greyish purple':'#887191','greyish teal':'#719f91','gross green':'#a0bf16','gunmetal':'#536267','hazel':'#8e7618','heather':'#a484ac','heliotrope':'#d94ff5','highlighter green':'#1bfc06','hospital green':'#9be5aa','hot green':'#25ff29','hot magenta':'#f504c9','hot pink':'#ff028d','hot purple':'#cb00f5','hunter green':'#0b4008','ice':'#d6fffa','ice blue':'#d7fffe','icky green':'#8fae22','indian red':'#850e04','indigo':'#380282','indigo blue':'#3a18b1','iris':'#6258c4','irish green':'#019529','ivory':'#ffffcb','jade':'#1fa774','jade green':'#2baf6a','jungle green':'#048243','kelley green':'#009337','kelly green':'#02ab2e','kermit green':'#5cb200','key lime':'#aeff6e','khaki':'#aaa662','khaki green':'#728639','kiwi':'#9cef43','kiwi green':'#8ee53f','lavender':'#c79fef','lavender blue':'#8b88f8','lavender pink':'#dd85d7','lawn green':'#4da409','leaf':'#71aa34','leaf green':'#5ca904','leafy green':'#51b73b','leather':'#ac7434','lemon':'#fdff52','lemon green':'#adf802','lemon lime':'#bffe28','lemon yellow':'#fdff38','lichen':'#8fb67b','light aqua':'#8cffdb','light aquamarine':'#7bfdc7','light beige':'#fffeb6','light blue':'#95d0fc','light blue green':'#7efbb3','light blue grey':'#b7c9e2','light bluish green':'#76fda8','light bright green':'#53fe5c','light brown':'#ad8150','light burgundy':'#a8415b','light cyan':'#acfffc','light eggplant':'#894585','light forest green':'#4f9153','light gold':'#fddc5c','light grass green':'#9af764','light green':'#96f97b','light green blue':'#56fca2','light greenish blue':'#63f7b4','light grey':'#d8dcd6','light grey blue':'#9dbcd4','light grey green':'#b7e1a1','light indigo':'#6d5acf','light khaki':'#e6f2a2','light lavendar':'#efc0fe','light lavender':'#dfc5fe','light light blue':'#cafffb','light light green':'#c8ffb0','light lilac':'#edc8ff','light lime':'#aefd6c','light lime green':'#b9ff66','light magenta':'#fa5ff7','light maroon':'#a24857','light mauve':'#c292a1','light mint':'#b6ffbb','light mint green':'#a6fbb2','light moss green':'#a6c875','light mustard':'#f7d560','light navy':'#155084','light navy blue':'#2e5a88','light neon green':'#4efd54','light olive':'#acbf69','light olive green':'#a4be5c','light orange':'#fdaa48','light pastel green':'#b2fba5','light pea green':'#c4fe82','light peach':'#ffd8b1','light periwinkle':'#c1c6fc','light pink':'#ffd1df','light plum':'#9d5783','light purple':'#bf77f6','light red':'#ff474c','light rose':'#ffc5cb','light royal blue':'#3a2efe','light sage':'#bcecac','light salmon':'#fea993','light sea green':'#98f6b0','light seafoam':'#a0febf','light seafoam green':'#a7ffb5','light sky blue':'#c6fcff','light tan':'#fbeeac','light teal':'#90e4c1','light turquoise':'#7ef4cc','light urple':'#b36ff6','light violet':'#d6b4fc','light yellow':'#fffe7a','light yellow green':'#ccfd7f','light yellowish green':'#c2ff89','lightblue':'#7bc8f6','lighter green':'#75fd63','lighter purple':'#a55af4','lightgreen':'#76ff7b','lightish blue':'#3d7afd','lightish green':'#61e160','lightish purple':'#a552e6','lightish red':'#fe2f4a','lilac':'#cea2fd','liliac':'#c48efd','lime':'#aaff32','lime green':'#89fe05','lime yellow':'#d0fe1d','lipstick':'#d5174e','lipstick red':'#c0022f','macaroni and cheese':'#efb435','magenta':'#c20078','mahogany':'#4a0100','maize':'#f4d054','mango':'#ffa62b','manilla':'#fffa86','marigold':'#fcc006','marine':'#042e60','marine blue':'#01386a','maroon':'#650021','mauve':'#ae7181','medium blue':'#2c6fbb','medium brown':'#7f5112','medium green':'#39ad48','medium grey':'#7d7f7c','medium pink':'#f36196','medium purple':'#9e43a2','melon':'#ff7855','merlot':'#730039','metallic blue':'#4f738e','mid blue':'#276ab3','mid green':'#50a747','midnight':'#03012d','midnight blue':'#020035','midnight purple':'#280137','military green':'#667c3e','milk chocolate':'#7f4e1e','mint':'#9ffeb0','mint green':'#8fff9f','minty green':'#0bf77d','mocha':'#9d7651','moss':'#769958','moss green':'#658b38','mossy green':'#638b27','mud':'#735c12','mud brown':'#60460f','mud green':'#606602','muddy brown':'#886806','muddy green':'#657432','muddy yellow':'#bfac05','mulberry':'#920a4e','murky green':'#6c7a0e','mushroom':'#ba9e88','mustard':'#ceb301','mustard brown':'#ac7e04','mustard green':'#a8b504','mustard yellow':'#d2bd0a','muted blue':'#3b719f','muted green':'#5fa052','muted pink':'#d1768f','muted purple':'#805b87','nasty green':'#70b23f','navy':'#01153e','navy blue':'#001146','navy green':'#35530a','neon blue':'#04d9ff','neon green':'#0cff0c','neon pink':'#fe019a','neon purple':'#bc13fe','neon red':'#ff073a','neon yellow':'#cfff04','nice blue':'#107ab0','night blue':'#040348','ocean':'#017b92','ocean blue':'#03719c','ocean green':'#3d9973','ocher':'#bf9b0c','ochre':'#bf9005','ocre':'#c69c04','off blue':'#5684ae','off green':'#6ba353','off white':'#ffffe4','off yellow':'#f1f33f','old pink':'#c77986','old rose':'#c87f89','olive':'#6e750e','olive brown':'#645403','olive drab':'#6f7632','olive green':'#677a04','olive yellow':'#c2b709','orange':'#f97306','orange brown':'#be6400','orange pink':'#ff6f52','orange red':'#fd411e','orange yellow':'#ffad01','orangeish':'#fd8d49','orangered':'#fe420f','orangey brown':'#b16002','orangey red':'#fa4224','orangey yellow':'#fdb915','orangish':'#fc824a','orangish brown':'#b25f03','orangish red':'#f43605','orchid':'#c875c4','pale':'#fff9d0','pale aqua':'#b8ffeb','pale blue':'#d0fefe','pale brown':'#b1916e','pale cyan':'#b7fffa','pale gold':'#fdde6c','pale green':'#c7fdb5','pale grey':'#fdfdfe','pale lavender':'#eecffe','pale light green':'#b1fc99','pale lilac':'#e4cbff','pale lime':'#befd73','pale lime green':'#b1ff65','pale magenta':'#d767ad','pale mauve':'#fed0fc','pale olive':'#b9cc81','pale olive green':'#b1d27b','pale orange':'#ffa756','pale peach':'#ffe5ad','pale pink':'#ffcfdc','pale purple':'#b790d4','pale red':'#d9544d','pale rose':'#fdc1c5','pale salmon':'#ffb19a','pale sky blue':'#bdf6fe','pale teal':'#82cbb2','pale turquoise':'#a5fbd5','pale violet':'#ceaefa','pale yellow':'#ffff84','parchment':'#fefcaf','pastel blue':'#a2bffe','pastel green':'#b0ff9d','pastel orange':'#ff964f','pastel pink':'#ffbacd','pastel purple':'#caa0ff','pastel red':'#db5856','pastel yellow':'#fffe71','pea':'#a4bf20','pea green':'#8eab12','pea soup':'#929901','pea soup green':'#94a617','peach':'#ffb07c','peachy pink':'#ff9a8a','peacock blue':'#016795','pear':'#cbf85f','periwinkle':'#8e82fe','periwinkle blue':'#8f99fb','perrywinkle':'#8f8ce7','petrol':'#005f6a','pig pink':'#e78ea5','pine':'#2b5d34','pine green':'#0a481e','pink':'#ff81c0','pink purple':'#db4bda','pink red':'#f5054f','pink/purple':'#ef1de7','pinkish':'#d46a7e','pinkish brown':'#b17261','pinkish grey':'#c8aca9','pinkish orange':'#ff724c','pinkish purple':'#d648d7','pinkish red':'#f10c45','pinkish tan':'#d99b82','pinky':'#fc86aa','pinky purple':'#c94cbe','pinky red':'#fc2647','piss yellow':'#ddd618','pistachio':'#c0fa8b','plum':'#580f41','plum purple':'#4e0550','poison green':'#40fd14','poo':'#8f7303','poo brown':'#885f01','poop':'#7f5e00','poop brown':'#7a5901','poop green':'#6f7c00','powder blue':'#b1d1fc','powder pink':'#ffb2d0','primary blue':'#0804f9','prussian blue':'#004577','puce':'#a57e52','puke':'#a5a502','puke brown':'#947706','puke green':'#9aae07','puke yellow':'#c2be0e','pumpkin':'#e17701','pumpkin orange':'#fb7d07','pure blue':'#0203e2','purple':'#7e1e9c','purple blue':'#632de9','purple brown':'#673a3f','purple grey':'#866f85','purple pink':'#e03fd8','purple red':'#990147','purple/blue':'#5d21d0','purple/pink':'#d725de','purpleish':'#98568d','purpleish blue':'#6140ef','purpleish pink':'#df4ec8','purpley':'#8756e4','purpley blue':'#5f34e7','purpley grey':'#947e94','purpley pink':'#c83cb9','purplish':'#94568c','purplish blue':'#601ef9','purplish brown':'#6b4247','purplish grey':'#7a687f','purplish pink':'#ce5dae','purplish red':'#b0054b','purply':'#983fb2','purply blue':'#661aee','purply pink':'#f075e6','putty':'#beae8a','racing green':'#014600','radioactive green':'#2cfa1f','raspberry':'#b00149','raw sienna':'#9a6200','raw umber':'#a75e09','really light blue':'#d4ffff','red':'#e50000','red brown':'#8b2e16','red orange':'#fd3c06','red pink':'#fa2a55','red purple':'#820747','red violet':'#9e0168','red wine':'#8c0034','reddish':'#c44240','reddish brown':'#7f2b0a','reddish grey':'#997570','reddish orange':'#f8481c','reddish pink':'#fe2c54','reddish purple':'#910951','reddy brown':'#6e1005','rich blue':'#021bf9','rich purple':'#720058','robin egg blue':'#8af1fe','robins egg':'#6dedfd','robins egg blue':'#98eff9','rosa':'#fe86a4','rose':'#cf6275','rose pink':'#f7879a','rose red':'#be013c','rosy pink':'#f6688e','rouge':'#ab1239','royal':'#0c1793','royal blue':'#0504aa','royal purple':'#4b006e','ruby':'#ca0147','russet':'#a13905','rust':'#a83c09','rust brown':'#8b3103','rust orange':'#c45508','rust red':'#aa2704','rusty orange':'#cd5909','rusty red':'#af2f0d','saffron':'#feb209','sage':'#87ae73','sage green':'#88b378','salmon':'#ff796c','salmon pink':'#fe7b7c','sand':'#e2ca76','sand brown':'#cba560','sand yellow':'#fce166','sandstone':'#c9ae74','sandy':'#f1da7a','sandy brown':'#c4a661','sandy yellow':'#fdee73','sap green':'#5c8b15','sapphire':'#2138ab','scarlet':'#be0119','sea':'#3c9992','sea blue':'#047495','sea green':'#53fca1','seafoam':'#80f9ad','seafoam blue':'#78d1b6','seafoam green':'#7af9ab','seaweed':'#18d17b','seaweed green':'#35ad6b','sepia':'#985e2b','shamrock':'#01b44c','shamrock green':'#02c14d','shit':'#7f5f00','shit brown':'#7b5804','shit green':'#758000','shocking pink':'#fe02a2','sick green':'#9db92c','sickly green':'#94b21c','sickly yellow':'#d0e429','sienna':'#a9561e','silver':'#c5c9c7','sky':'#82cafc','sky blue':'#75bbfd','slate':'#516572','slate blue':'#5b7c99','slate green':'#658d6d','slate grey':'#59656d','slime green':'#99cc04','snot':'#acbb0d','snot green':'#9dc100','soft blue':'#6488ea','soft green':'#6fc276','soft pink':'#fdb0c0','soft purple':'#a66fb5','spearmint':'#1ef876','spring green':'#a9f971','spruce':'#0a5f38','squash':'#f2ab15','steel':'#738595','steel blue':'#5a7d9a','steel grey':'#6f828a','stone':'#ada587','stormy blue':'#507b9c','straw':'#fcf679','strawberry':'#fb2943','strong blue':'#0c06f7','strong pink':'#ff0789','sun yellow':'#ffdf22','sunflower':'#ffc512','sunflower yellow':'#ffda03','sunny yellow':'#fff917','sunshine yellow':'#fffd37','swamp':'#698339','swamp green':'#748500','tan':'#d1b26f','tan brown':'#ab7e4c','tan green':'#a9be70','tangerine':'#ff9408','taupe':'#b9a281','tea':'#65ab7c','tea green':'#bdf8a3','teal':'#029386','teal blue':'#01889f','teal green':'#25a36f','tealish':'#24bca8','tealish green':'#0cdc73','terra cotta':'#c9643b','terracota':'#cb6843','terracotta':'#ca6641','tiffany blue':'#7bf2da','tomato':'#ef4026','tomato red':'#ec2d01','topaz':'#13bbaf','toupe':'#c7ac7d','toxic green':'#61de2a','tree green':'#2a7e19','true blue':'#010fcc','true green':'#089404','turquoise':'#06c2ac','turquoise blue':'#06b1c4','turquoise green':'#04f489','turtle green':'#75b84f','twilight':'#4e518b','twilight blue':'#0a437a','ugly blue':'#31668a','ugly brown':'#7d7103','ugly green':'#7a9703','ugly pink':'#cd7584','ugly purple':'#a442a0','ugly yellow':'#d0c101','ultramarine':'#2000b1','ultramarine blue':'#1805db','umber':'#b26400','velvet':'#750851','vermillion':'#f4320c','very dark blue':'#000133','very dark brown':'#1d0200','very dark green':'#062e03','very dark purple':'#2a0134','very light blue':'#d5ffff','very light brown':'#d3b683','very light green':'#d1ffbd','very light pink':'#fff4f2','very light purple':'#f6cefc','very pale blue':'#d6fffe','very pale green':'#cffdbc','vibrant blue':'#0339f8','vibrant green':'#0add08','vibrant purple':'#ad03de','violet':'#9a0eea','violet blue':'#510ac9','violet pink':'#fb5ffc','violet red':'#a50055','viridian':'#1e9167','vivid blue':'#152eff','vivid green':'#2fef10','vivid purple':'#9900fa','vomit':'#a2a415','vomit green':'#89a203','vomit yellow':'#c7c10c','warm blue':'#4b57db','warm brown':'#964e02','warm grey':'#978a84','warm pink':'#fb5581','warm purple':'#952e8f','washed out green':'#bcf5a6','water blue':'#0e87cc','watermelon':'#fd4659','weird green':'#3ae57f','wheat':'#fbdd7e','white':'#ffffff','windows blue':'#3778bf','wine':'#80013f','wine red':'#7b0323','wintergreen':'#20f986','wisteria':'#a87dc2','yellow':'#ffff14','yellow brown':'#b79400','yellow green':'#c0fb2d','yellow ochre':'#cb9d06','yellow orange':'#fcb001','yellow tan':'#ffe36e','yellow/green':'#c8fd3d','yellowgreen':'#bbf90f','yellowish':'#faee66','yellowish brown':'#9b7a01','yellowish green':'#b0dd16','yellowish orange':'#ffab0f','yellowish tan':'#fcfc81','yellowy brown':'#ae8b0c','yellowy green':'#bff128'};
