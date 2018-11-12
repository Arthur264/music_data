let app = {
    file_size: [],
    files_process: [],
    socket: function () {
        let self = this;
        let socket = io.connect(`http://${document.domain}:${location.port}`);
        socket.on('file_size', function (data) {
            app.file_size = Array.isArray(data) ? data: app.update_items(self.file_size, data);
            self.template_items(self.file_size, 'show_file_size', 'Crawler file size');
        });

        socket.on('memory', function (data) {
            if (Array.isArray(data)) {
                self.init_memory_line(data);
                return false;
            }
            self.change_memory_line(data);
        });
        socket.on('process_item', function (data) {
            app.files_process = Array.isArray(data) ? data: app.update_items(self.files_process, data);
            app.template_items(self.files_process, 'show_file_process', 'Process items');
        });
    },
    update_items: function (items, data) {
        let present_in_arr = false;
        for (let i = 0; i < items.length; i++) {
            let item = items[i];
            if (item['file_type'] === data['file_type']) {
                if (!('spider_name' in item) || item['spider_name'] === data['spider_name']) {
                    items[i] = Object.assign({}, item, data);
                    present_in_arr = true;
                }
            }
        }
        if (!present_in_arr) {
            items.push(data)
        }
        return items;
    },
    init_memory_line: function (data) {
        let result = {};
        for (let i = 0; i < data.length; i++) {
            let spider_name = data[i]['spider_name'];
            let memory = data[i]['memory'];
            app.config.data.labels.push(data[i]['time']);
            if (spider_name in result) {
                result[spider_name].push(memory);
            } else {
                result[spider_name] = [memory]
            }
        }
        for (let prop in result) {
            app.config.data.datasets.push(this.generateDataset(prop, result[prop]));
        }
        console.log(window.memoryLine);
        window.memoryLine.update();
    },
    chart: function () {
        this.config = {
            type: 'line',
            data: {
                labels: [],
                datasets: [],
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
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Memory'
                        }
                    }]
                }
            }
        };
        let ctx = document.getElementById('canvas').getContext('2d');
        window.memoryLine = new Chart(ctx, app.config);
    },
    template_items: function (items, template_name, title) {
        $(`#${template_name}`).html('');
        let templates = [];
        let source = '<div class="col-xl-6 col-lg-6"><div class="card"><div class="card-body"><div class="text-center">{{this.title}}</div> <div class="stat-widget-one"><div class="stat-icon dib"><i class="ti-layout-grid2 text-warning border-warning"></i></div><div class="stat-content dib"><div class="stat-text">{{this.spider_name}} {{this.file_type}}</div><div class="stat-digit">{{size}}  {{count}}</div></div></div></div></div></div>';
        for (let i = items.length - 1; i >= 0; i--) {
            let template = Handlebars.compile(source);
            items[i].title = title;
            templates.push(template(items[i]));
        }
        templates.forEach(function (item) {
            $(`#${template_name}`).append(item);
        });
    },
    change_memory_line: function (item) {
        let item_in_dataset = false;
        app.config.data.datasets.forEach(function (dataset) {
            if (dataset['label'] === item['spider_name']) {
                app.config.data.labels.push(item['time']);
                dataset.data.push(item['memory']);
                item_in_dataset = true;
            }
        });

        if (!item_in_dataset) {
            app.config.data.datasets.push(this.generateDataset(item['spider_name']));
        }
        window.memoryLine.update();
    },
    generateDataset: function (name, data = []) {
        return {
            label: name,
            backgroundColor: this.randomColor(),
            borderColor: this.randomColor(),
            data: data,
            fill: false,
        }
    },
    randomColor: function () {
        let keys = Object.keys(window.chartColors);
        return window.chartColors[keys[keys.length * Math.random() << 0]];
    },
    init: function () {
        this.chart();
        this.socket();
    }

};

$(document).ready(function () {
    app.init()

});