<template>
    <section>
        <b-field label="SQL Query">
            <b-input type="textarea" v-model="replica.query"></b-input>
        </b-field>
        <b-message type="is-success" :active.sync="replica.result_show">
            Result: <strong>{{ replica.result }}</strong>
        </b-message>
        <button 
            class="button is-primary " 
            :class="{ 'is-loading': replica.loading }"
            @click="attemptRunQuery">
            Run
        </button>
        <hr>
        <b-field label="Insert Sample Data">
            <b-numberinput v-model="replica.insert_number"></b-numberinput>
        </b-field>
        <button 
            class="button is-primary is-mt-3" 
            :class="{ 'is-loading': replica.insert_loading }"
            @click="attemptRunInsert">
            Insert
        </button>
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
                    insert_number: 0,
                    result: '',
                    result_show: false,
                    item: [],
                    loading: false,
                    insert_loading: false,
                },
            }
        },
        methods: {
            attemptRunInsert() {
                this.replica.insert_loading = true
                this.runInsert()
            },
            runInsert() {
                let that = this
                let data = {
                    number: that.replica.insert_number,
                }
                let url = that.replica.url + 'insert/'
                axios.post(url, data)
                    .then(function (response) {
                        that.$toast.open({
                            duration: 5000,
                            message: 'Insert operation is started',
                            position: 'is-bottom',
                            type: 'is-primary'
                        })                    
                    })
                    .catch(function (error) {
                        console.log(error);
                    })
                    .finally(function() {
                        that.replica.insert_loading = false
                    })
            },
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
