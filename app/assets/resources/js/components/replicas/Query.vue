<template>
    <section>
        <b-field label="SQL Query">
            <b-input type="textarea" v-model="replica.query"></b-input>
        </b-field>
        <b-message type="is-success" :active.sync="replica.result_show">
            Result: <strong>{{ replica.result }}</strong>
        </b-message>
        <button 
            class="button is-primary is-pulled-right" 
            :class="{ 'is-loading': replica.loading }"
            @click="attemptRunQuery">Run</button>
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
                    url: '/api/v1/replicas/query/',
                    query: '{"location" : "US", "factoryId" : {"$gte" : 1500}}',
                    result: '',
                    result_show: false,
                    item: [],
                    loading: false,
                },
            }
        },
        methods: {
            attemptRunQuery() {
                this.replica.loading = true
                this.runQuery()
            },
            runQuery() {
                let that = this
                let data = {
                    query: that.replica.query,
                }
                axios.post(that.replica.url, data)
                    .then(function (response) {
                        that.replica.result = response.data.result
                        that.replica.result_show = true
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
