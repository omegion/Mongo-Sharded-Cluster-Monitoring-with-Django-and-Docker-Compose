<template>
    <section>
        <div id="chart">
            <apexchart type=area height=350 :options="chartOptions" :series="series" />
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
            }, 1000);   
        },
        methods: {
            attemptLoadReplica() {
                this.replica.loading = true
                this.loadReplica()
            },
            loadReplica() {
                let that = this
                let url = that.replica.url+'?replica_id='+that.replicaId
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
