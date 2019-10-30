from python_pachyderm.proto.pps import pps_pb2 as pps_proto
from python_pachyderm.proto.pps import pps_pb2_grpc as pps_grpc
from python_pachyderm.util import commit_from


class PPSMixin:
    @property
    def _pps_stub(self):
        if not hasattr(self, "__pps_stub"):
            self.__pps_stub = self._create_stub(pps_grpc)
        return self.__pps_stub

    def inspect_job(self, job_id, block_state=None, output_commit=None):
        """
        Inspects a job with a given ID. Returns a `JobInfo`.

        Params:

        * `job_id`: The ID of the job to inspect.
        * `block_state`: If true, block until the job completes.
        * `output_commit`: An optional tuple, string, or `Commit` object
        representing an output commit to filter on.
        """

        output_commit = commit_from(output_commit) if output_commit is not None else None
        req = pps_proto.InspectJobRequest(job=pps_proto.Job(id=job_id),
                                          block_state=block_state,
                                          output_commit=output_commit)
        return self._pps_stub.InspectJob(req, metadata=self.metadata)

    def list_job(self, pipeline_name=None, input_commit=None, output_commit=None, history=None):
        """
        Lists jobs. Yields `JobInfo` objects.

        Params:

        * `pipeline_name`: An optional string representing a pipeline name to
        filter on.
        * `input_commit`: An optional list of tuples, strings, or `Commit`
        objects representing input commits to filter on.
        * `output_commit`: An optional tuple, string, or `Commit` object
        representing an output commit to filter on.
        * `history`: An optional int that indicates to return jobs from
          historical versions of pipelines. Semantics are:
            * 0: Return jobs from the current version of the pipeline or
              pipelines.
            * 1: Return the above and jobs from the next most recent version
            * 2: etc.
            * -1: Return jobs from all historical versions.
        """

        pipeline = pps_proto.Pipeline(name=pipeline_name) if pipeline_name is not None else None

        if isinstance(input_commit, list):
            input_commit = [commit_from(ic) for ic in input_commit]
        elif input_commit is not None:
            input_commit = [commit_from(input_commit)]

        output_commit = commit_from(output_commit) if output_commit is not None else None

        req = pps_proto.ListJobRequest(pipeline=pipeline, input_commit=input_commit,
                                       output_commit=output_commit, history=history)

        return self._pps_stub.ListJobStream(req, metadata=self.metadata)

    def flush_job(self, commits, pipeline_names=None):
        """
        Blocks until all of the jobs which have a set of commits as
        provenance have finished. Yields `JobInfo` objects.

        Params:

        * `commits`: A list of tuples, strings, or `Commit` objects
        representing the commits to flush.
        * `pipeline_names`: An optional list of strings specifying pipeline
        names. If specified, only jobs within these pipelines will be flushed.
        """

        commits = [commit_from(c) for c in commits]
        pipelines = [pps_proto.Pipeline(name=name) for name in pipeline_names] if pipeline_names is not None else None
        req = pps_proto.FlushJobRequest(commits=commits, to_pipelines=pipelines)
        return self._pps_stub.FlushJob(req)

    def delete_job(self, job_id):
        """
        Deletes a job by its ID.

        Params:

        * `job_id`: The ID of the job to delete.
        """

        req = pps_proto.DeleteJobRequest(job=pps_proto.Job(id=job_id))
        self._pps_stub.DeleteJob(req, metadata=self.metadata)

    def stop_job(self, job_id):
        """
        Stops a job by its ID.

        Params:

        * `job_id`: The ID of the job to stop.
        """

        req = pps_proto.StopJobRequest(job=pps_proto.Job(id=job_id))
        self._pps_stub.StopJob(req, metadata=self.metadata)

    def inspect_datum(self, job_id, datum_id):
        """
        Inspects a datum. Returns a `DatumInfo` object.

        Params:

        * `job_id`: The ID of the job.
        * `datum_id`: The ID of the datum.
        """

        req = pps_proto.InspectDatumRequest(datum=pps_proto.Datum(id=datum_id, job=pps_proto.Job(id=job_id)))
        return self._pps_stub.InspectDatum(req, metadata=self.metadata)

    def list_datum(self, job_id, page_size=None, page=None):
        """
        Lists datums. Yields `ListDatumStreamResponse` objects.

        Params:

        * `job_id`: The ID of the job.
        * `page_size`: An optional int specifying the size of the page.
        * `page`: An optional int specifying the page number.
        """

        req = pps_proto.ListDatumRequest(job=pps_proto.Job(id=job_id), page_size=page_size, page=page)
        return self._pps_stub.ListDatumStream(req, metadata=self.metadata)

    def restart_datum(self, job_id, data_filters=None):
        """
        Restarts a datum.

        Params:

        * `job_id`: The ID of the job.
        * `data_filters`: An optional iterable of strings.
        """

        req = pps_proto.RestartDatumRequest(job=pps_proto.Job(id=job_id), data_filters=data_filters)
        self._pps_stub.RestartDatum(req, metadata=self.metadata)

    def create_pipeline(self, pipeline_name, transform=None, parallelism_spec=None,
                        hashtree_spec=None, egress=None, update=None, output_branch=None,
                        scale_down_threshold=None, resource_requests=None,
                        resource_limits=None, input=None, description=None, cache_size=None,
                        enable_stats=None, reprocess=None, max_queue_size=None,
                        service=None, chunk_spec=None, datum_timeout=None,
                        job_timeout=None, salt=None, standby=None, datum_tries=None,
                        scheduling_spec=None, pod_patch=None, spout=None):
        """
        Creates a pipeline. For more info, please refer to the pipeline spec
        document:
        http://docs.pachyderm.io/en/latest/reference/pipeline_spec.html

        Params:

        * `pipeline_name`: A string representing the pipeline name.
        * `transform`: An optional `Transform` object.
        * `parallelism_spec`: An optional `ParallelismSpec` object.
        * `hashtree_spec`: An optional `HashtreeSpec` object.
        * `egress`: An optional `Egress` object.
        * `update`: An optional bool specifying whether this should behave as
        an upsert.
        * `output_branch`: An optional string representing the branch to output
        results on.
        * `scale_down_threshold`: An optional pps_proto.uf `Duration` object.
        * `resource_requests`: An optional `ResourceSpec` object.
        * `resource_limits`: An optional `ResourceSpec` object.
        * `input`: An optional `Input` object.
        * `description`: An optional string describing the pipeline.
        * `cache_size`: An optional string.
        * `enable_stats`: An optional bool.
        * `reprocess`: An optional bool. If true, pachyderm forces the pipeline
        to reprocess all datums. It only has meaning if `update` is `True`.
        * `max_queue_size`: An optional int.
        * `service`: An optional `Service` object.
        * `chunk_spec`: An optional `ChunkSpec` object.
        * `datum_timeout`: An optional pps_proto.uf `Duration` object.
        * `job_timeout`: An optional pps_proto.uf `Duration` object.
        * `salt`: An optional stirng.
        * `standby`: An optional bool.
        * `datum_tries`: An optional int.
        * `scheduling_spec`: An optional `SchedulingSpec` object.
        * `pod_patch`: An optional string.
        * `spout`: An optional `Spout` object.
        """

        req = pps_proto.CreatePipelineRequest(
            pipeline=pps_proto.Pipeline(name=pipeline_name),
            transform=transform, parallelism_spec=parallelism_spec,
            hashtree_spec=hashtree_spec, egress=egress, update=update,
            output_branch=output_branch, scale_down_threshold=scale_down_threshold,
            resource_requests=resource_requests, resource_limits=resource_limits,
            input=input, description=description, cache_size=cache_size,
            enable_stats=enable_stats, reprocess=reprocess,
            max_queue_size=max_queue_size, service=service,
            chunk_spec=chunk_spec, datum_timeout=datum_timeout,
            job_timeout=job_timeout, salt=salt, standby=standby,
            datum_tries=datum_tries, scheduling_spec=scheduling_spec,
            pod_patch=pod_patch, spout=spout,
        )
        self._pps_stub.CreatePipeline(req, metadata=self.metadata)

    def inspect_pipeline(self, pipeline_name, history=None):
        """
        Inspects a pipeline. Returns a `PipelineInfo` object.

        Params:

        * `pipeline_name`: A string representing the pipeline name.
        * `history`: An optional int that indicates to return jobs from
        historical versions of pipelines. Semantics are:
            * 0: Return jobs from the current version of the pipeline or
              pipelines.
            * 1: Return the above and jobs from the next most recent version
            * 2: etc.
            * -1: Return jobs from all historical versions.
        """

        pipeline = pps_proto.Pipeline(name=pipeline_name)

        if history is None:
            req = pps_proto.InspectPipelineRequest(pipeline=pipeline)
            return self._pps_stub.InspectPipeline(req, metadata=self.metadata)
        else:
            # `InspectPipeline` doesn't support history, but `ListPipeline`
            # with a pipeline filter does, so we use that here
            req = pps_proto.ListPipelineRequest(pipeline=pipeline, history=history)
            pipelines = self._pps_stub.ListPipeline(req, metadata=self.metadata).pipeline_info
            assert len(pipelines) <= 1
            return pipelines[0] if len(pipelines) else None

    def list_pipeline(self, history=None):
        """
        Lists pipelines. Returns a `PipelineInfos` object.

        Params:

        * `pipeline_name`: A string representing the pipeline name.
        * `history`: An optional int that indicates to return jobs from
        historical versions of pipelines. Semantics are:
            * 0: Return jobs from the current version of the pipeline or
              pipelines.
            * 1: Return the above and jobs from the next most recent version
            * 2: etc.
            * -1: Return jobs from all historical versions.
        """
        req = pps_proto.ListPipelineRequest(history=history)
        return self._pps_stub.ListPipeline(req, metadata=self.metadata)

    def delete_pipeline(self, pipeline_name, force=None):
        """
        Deletes a pipeline.

        Params:

        * `pipeline_name`: A string representing the pipeline name.
        * `force`: Whether to force delete.
        """

        req = pps_proto.DeletePipelineRequest(pipeline=pps_proto.Pipeline(name=pipeline_name), force=force)
        self._pps_stub.DeletePipeline(req, metadata=self.metadata)

    def delete_all_pipelines(self, force=None):
        """
        Deletes all pipelines.

        Params:

        * `force`: Whether to force delete.
        """

        req = pps_proto.DeletePipelineRequest(all=True, force=force)
        self._pps_stub.DeletePipeline(req, metadata=self.metadata)

    def start_pipeline(self, pipeline_name):
        """
        Starts a pipeline.

        Params:

        * `pipeline_name`: A string representing the pipeline name.
        """

        req = pps_proto.StartPipelineRequest(pipeline=pps_proto.Pipeline(name=pipeline_name))
        self._pps_stub.StartPipeline(req, metadata=self.metadata)

    def stop_pipeline(self, pipeline_name):
        """
        Stops a pipeline.

        Params:

        * `pipeline_name`: A string representing the pipeline name.
        """
        req = pps_proto.StopPipelineRequest(pipeline=pps_proto.Pipeline(name=pipeline_name))
        self._pps_stub.StopPipeline(req, metadata=self.metadata)

    def run_pipeline(self, pipeline_name, provenance=None):
        """
        Runs a pipeline.

        Params:

        * `pipeline_name`: A string representing the pipeline name.
        * `provenance`: An optional iterable of `CommitProvenance` objects
        representing the pipeline execution provenance.
        """
        req = pps_proto.RunPipelineRequest(
            pipeline=pps_proto.Pipeline(name=pipeline_name),
            provenance=provenance,
        )
        self._pps_stub.RunPipeline(req, metadata=self.metadata)

    def delete_all(self):
        """
        Deletes everything in pachyderm.
        """
        req = pps_proto.google_dot_pps_proto.uf_dot_empty__pb2.Empty()
        self._pps_stub.DeleteAll(req, metadata=self.metadata)

    def get_pipeline_logs(self, pipeline_name, data_filters=None, master=None,
                          datum=None, follow=None, tail=None):
        """
        Gets logs for a pipeline. Yields `LogMessage` objects.

        Params:

        * `pipeline_name`: A string representing a pipeline to get
        logs of.
        * `data_filters`: An optional iterable of strings specifying the names
        of input files from which we want processing logs. This may contain
        multiple files, to query pipelines that contain multiple inputs. Each
        filter may be an absolute path of a file within a pps repo, or it may
        be a hash for that file (to search for files at specific versions.)
        * `master`: An optional bool.
        * `datum`: An optional `Datum` object.
        * `follow`: An optional bool specifying whether logs should continue to
        stream forever.
        * `tail`: An optional int. If nonzero, the number of lines from the end
        of the logs to return.  Note: tail applies per container, so you will
        get tail * <number of pods> total lines back.
        """

        req = pps_proto.GetLogsRequest(
            pipeline=pps_proto.Pipeline(name=pipeline_name),
            data_filters=data_filters, master=master, datum=datum,
            follow=follow, tail=tail,
        )
        return self._pps_stub.GetLogs(req, metadata=self.metadata)

    def get_job_logs(self, job_id, data_filters=None, datum=None, follow=None,
                     tail=None):
        """
        Gets logs for a job. Yields `LogMessage` objects.

        Params:

        * `job_id`: A string representing a job to get logs of.
        * `data_filters`: An optional iterable of strings specifying the names
        of input files from which we want processing logs. This may contain
        multiple files, to query pipelines that contain multiple inputs. Each
        filter may be an absolute path of a file within a pps repo, or it may
        be a hash for that file (to search for files at specific versions.)
        * `datum`: An optional `Datum` object.
        * `follow`: An optional bool specifying whether logs should continue to
        stream forever.
        * `tail`: An optional int. If nonzero, the number of lines from the end
        of the logs to return.  Note: tail applies per container, so you will
        get tail * <number of pods> total lines back.
        """

        req = pps_proto.GetLogsRequest(
            job=pps_proto.Job(id=job_id), data_filters=data_filters, datum=datum,
            follow=follow, tail=tail,
        )
        return self._pps_stub.GetLogs(req, metadata=self.metadata)

    def garbage_collect(self):
        """
        Runs garbage collection.
        """
        return self._pps_stub.GarbageCollect(pps_proto.GarbageCollectRequest(), metadata=self.metadata)
