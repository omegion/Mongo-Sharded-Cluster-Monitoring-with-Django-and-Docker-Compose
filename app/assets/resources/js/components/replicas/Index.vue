<template>
    <div class="columns">
        <div class="column is-8">
            <div class="content is-medium">
                <h3 class="title is-3">Replica Set</h3>
                <div class="box" v-for="replica_row in replica.items" :key="replica_row.id">
                    <h4 id="const" class="title is-3">
                        {{ replica_row.name }}
                        <b-tag v-if="replica_row.state == 'PRIMARY'" type="is-primary">{{ replica_row.state }}</b-tag>
                        <b-tag v-else>{{ replica_row.state }}</b-tag>
                        <b-dropdown aria-role="list" class="is-pulled-right">
                            <button class="button is-primary" slot="trigger">
                                <b-icon icon="menu-down"></b-icon>
                            </button>

                            <b-dropdown-item aria-role="listitem" @click="attemptDropReplica(replica_row.id)">Drop Primary</b-dropdown-item>
                        </b-dropdown>
                    </h4>
                    <chart :replica-id="replica_row.id" :key="replica_row.id"></chart>
                </div>
            </div>
        </div>
        <div class="column is-4">
            <div class="content is-medium">
                <h3 class="title is-3">Query</h3>
                <div class="box is-pb-5">
                    <query></query>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Chart from './Chart.vue'
    import Query from './Query.vue'

    export default {
        components: {
            'chart': Chart,
            'query': Query,
        },
        props: {
            userId: {
                type: Number,
                default: 0
            },
        },
        data () {
            return {
                replica: {
                    url: '/api/v1/replicas/',
                    items: [],
                    loading: false,
                },
            }
        },
        mounted() {
            this.attemptLoadReplicas()           
            setInterval(() => {
                this.attemptLoadReplicas()           
            }, 1000);
        },
        methods: {
            attemptDropReplica(replica_id) {
                this.replica.loading = true
                this.dropReplica(replica_id)
            },
            dropReplica: _.debounce(function (replica_id) {
                let that = this
                let url = that.replica.url+replica_id+'/drop/'
                axios.post(url)
                    .then(function (response) {
                        that.$toast.open({
                            duration: 5000,
                            message: 'Replica is dropped from PRIMARY state',
                            position: 'is-bottom',
                            type: 'is-primary'
                        })
                    })
                    .catch(function (error) {
                        console.log(error);
                    })
                    .finally(function() {
                        that.replica.loading = false
                    })
            }, 250),
            attemptLoadReplicas() {
                this.replica.loading = true
                this.loadReplicas()
            },
            loadReplicas: _.debounce(function (e) {
                let that = this
                let url = that.replica.url+'?page_size=99'
                axios.get(url)
                    .then(function (response) {
                        that.replica.items = response.data.results
                    })
                    .catch(function (error) {
                        console.log(error);
                    })
                    .finally(function() {
                        that.replica.loading = false
                    })
            }, 250),
        },
    }
</script>
