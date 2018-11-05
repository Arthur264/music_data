let app = {
	memory: [],
	file_size: [],
    socket: function () {
    	let self = this;
        let socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('file_size', function (data) {
            if (Array.isArray(data)){
                app.file_size = data;
                return false;
            }
        	let present_in_arr = false;
        	for (var i = 0; i < self.file_size.length; i++) {
        		let item = self.file_size[i];
        		if(item['spider_name'] === data['spider_name'] && item['file_type'] === data['file_type']){
        			item = Object.assign({}, item, data);
        			present_in_arr = true;
        			self.file_size[i] = item;
        		};
        	}
        	if(!present_in_arr){
        		self.file_size.push(data)
        	}
        	self.template_file_size();
        });

        socket.on('memory', function (data) {
            if (Array.isArray(data)){
                this.init_memory_line(data);
                return false;
            }
            app.memory.push(data)
            self.change_memory_line(data);
        });
    },
    init_memory_line: function(data){
        let result = {};
        for(let i=0; i< data.length; i++){
            spider_name = data['spider_name']
            if (spider_name in result){
                result[spider_name].push(data['memory']);
            }else{
                result[spider_name] = [data['memory']]
            }
        }
        this.memory = result;
        this.memory.forEach(function(item) {
        	if(dataset['label'] == item['spider_name']){
        		app.config.data.labels.push(item['time']);
        		dataset.data.push(item['memory']);
        		item_in_dataset = true;
        	}
		});

    },
    chart: function(){
		this.config = {
			type: 'line',
			data: {
				labels: [],
				datasets: []
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Memory used'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						type: "time",
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Time'
						}
					}],
					yAxes: [{
						display: true,
						ticks: {
                                beginAtZero: true,
                                steps: 10,
                                stepValue: 5,
                                max: 100
                        },
						scaleLabel: {
							display: true,
							labelString: 'Memory'
						}
					}]
				}
			}
		};

		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.memoryLine = new Chart(ctx, app.config);
		};
    },
    template_file_size: function () {
    	$('#show_file_size').html('');
    	let templates = [];
    	let source = '<div class="col-xl-6 col-lg-6"><div class="card"><div class="card-body"><div class="stat-widget-one"><div class="stat-icon dib"><i class="ti-layout-grid2 text-warning border-warning"></i></div><div class="stat-content dib"><div class="stat-text">{{this.spider_name}}: {{this.file_type}}</div><div class="stat-digit">{{size}}  {{count}}</div></div></div></div></div></div>'
		for (let i = this.file_size.length - 1; i >= 0; i--) {
			let template = Handlebars.compile(source);
			templates.push(template(this.file_size[i]));
		};
		templates.forEach(function (item) {
			$('#show_file_size').append(item);
		});
    },
    change_memory_line: function(item) {
        let item_in_dataset = false;
        app.config.data.datasets.forEach(function(dataset) {
        	if(dataset['label'] == item['spider_name']){
        		app.config.data.labels.push(item['time']);
        		dataset.data.push(item['memory']);
        		item_in_dataset = true;
        	}
		});

		if(!item_in_dataset){
			app.config.data.datasets.push(this.generateDataset(item['spider_name']));
		}
		window.memoryLine.update();
    },
    generateDataset: function (name) {
    	return {
			label: name,
			backgroundColor: this.randomColor(),
			borderColor: this.randomColor(),
			data: [],
			fill: false,
		}
    },
    randomColor: function () {
	    var keys = Object.keys(window.chartColors )
	    return window.chartColors[keys[keys.length * Math.random() << 0]];
	},
    init: function () {
        this.socket();
        this.chart();
        this.template_file_size();
    }

}

$(document).ready(function () {
    app.init()

})