# Copyright 2018-2019 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pipeline construction."""

from typing import Dict

from kedro.pipeline import node, Pipeline
from gfg.nodes.data_engineering import (
    unzip,
    make_clean,
    feature_engineering
)
from gfg.nodes.data_science import (
    cluster,
    preprocess_for_classification,
    split_train_test,
    train_model,
    make_predictions
)

# Here you can define your data-driven pipeline by importing your functions
# and adding them to the pipeline as follows:
#
# from nodes.data_wrangling import clean_data, compute_features
#
# pipeline = Pipeline([
#     node(clean_data, 'customers', 'prepared_customers'),
#     node(compute_features, 'prepared_customers', ['X_train', 'Y_train'])
# ])
#
# Once you have your pipeline defined, you can run it from the root of your
# project by calling:
#
# $ kedro run


def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    de_pipeline = Pipeline(
        [
            node(unzip, 
            	 None, 
            	 'json_data', 
            	 name = 'unzip'),
            node(make_clean, 
            	 'json_data', 
            	 'clean_data', 
            	 name = 'make clean'),
            node(feature_engineering, 
            	 'clean_data', 
            	 'clean_data_with_fe', 
            	 name = 'feature engineering'),
        ]
    )

    ds_pipeline = Pipeline(
        [
            node(cluster, 
            	 ['parameters','clean_data_with_fe'], 
            	 ['cluster_model', 'clean_data_with_fe_labels'], 
            	 name = 'cluster'),
            node(preprocess_for_classification, 
            	 'clean_data_with_fe_labels', 
            	 'clean_data_with_fe_classification', 
            	 name = 'preprocess'),
            node(split_train_test, 
            	 ['parameters','clean_data_with_fe_classification'], 
            	 ['scaler', 'X_train_norm', 'X_test_norm', 'y_train', 'y_test'], 
            	 name = 'train test split'),
            node(train_model, 
            	 ['parameters', 'X_train_norm', 'X_test_norm', 'y_train', 'y_test'], 
            	 'classifier', 
            	 name = 'train'),
            node(make_predictions, 
            	 ['scaler', 'classifier', 'clean_data_with_fe_classification'], 
            	 'submission', 
            	 name = 'score'),
        ]
    )

    return {"de" : de_pipeline, "ds" : ds_pipeline, "__default__": de_pipeline + ds_pipeline}

