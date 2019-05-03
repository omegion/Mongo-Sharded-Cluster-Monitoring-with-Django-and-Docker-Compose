<template>
    <section>
        <div id="chart">
            <apexchart ref="realtimeChart" type=area height=350 :options="chartOptions" :series="series" />
        </div>
    </section>
</template>

<script>
    import VueApexCharts from 'vue-apexcharts'

    export default {
        components: {
            'apexchart': VueApexCharts,
        },
        props: {
            replicaId: {
                type: Number,
                default: 0
            },
        },
        data () {
            return {
                replica: {
                    url: '/api/v1/replicas/checks/',
                    item: [],
                    loading: false,
                },
                series: [
                    {
                        name: 'CPU',
                        data: []
                    }, 
                    {
                        name: 'Memory',
                        data: []
                    },
                ],
                chartOptions: {
                     chart: {
                        animations: {
                            enabled: true,
                            easing: 'linear',
                            dynamicAnimation: {
                                speed: 3000
                            }
                        },
                        toolbar: {
                            show: false
                        },
                        zoom: {
                            enabled: false
                        }
                    },
                    dataLabels: {
                        enabled: false
                    },
                    stroke: {
                        curve: 'smooth'
                    },
                    xaxis: {
                        type: 'datetime',
                        categories: [],
                    },
                    tooltip: {
                        x: {
                            format: 'dd/MM/yy HH:mm:ss'
                        },
                    }
                },
            }
        },
        mounted() {
            this.attemptLoadReplica()        
            setInterval(() => {
                this.attemptLoadReplica()           
            }, 3000);   
        },
        methods: {
            attemptLoadReplica() {
                this.replica.loading = true
                this.loadReplica()
            },
            loadReplica() {
                let that = this
                let url = that.replica.url+'?page_size=500&replica_id='+that.replicaId
                axios.get(url)
                    .then(function (response) {
                        that.replica.items = response.data.results
                        that.series[0].data = that.replica.items.map((check) => {
                            return {
                                x: check.created_at,
                                y: parseFloat(check.cpu).toFixed(1),
                            }
                        })
                        that.series[1].data = that.replica.items.map((check) => {
                            return {
                                x: check.created_at,
                                y: parseFloat(check.memory).toFixed(1),
                            }
                        })
                    })
                    .catch(function (error) {
                        console.log(error);
                    })
                    .finally(function() {
                        that.replica.loading = false
                    })
            },
        },
    }
</script>
