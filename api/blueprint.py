# -*- coding: utf-8 -*-
"""
    Customizing Blueprint for version support

    flask.blueprints
    ~~~~~~~~~~~~~~~~

    Blueprints are the recommended way to implement larger or more
    pluggable applications in Flask 0.7 and later.

    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""
import flask.blueprints

from config import API_PREFIX


class Blueprint(flask.blueprints.Blueprint):
    """Represents a blueprint.  A blueprint is an object that records
    functions that will be called with the
    :class:`~flask.blueprints.BlueprintSetupState` later to register functions
    or other things on the main application.  See :ref:`blueprints` for more
    information.

    .. versionadded:: 0.7
    """

    def __init__(self, name, import_name, api_prefix=None, **kwargs):
        super(Blueprint, self).__init__(name, import_name, **kwargs)
        self.api_prefix = api_prefix

    def route(self, rule, version=1, **options):
        # pylint:disable=arguments-differ
        """Like :meth:`Flask.route` but for a blueprint.  The endpoint for the
        :func:`url_for` function is prefixed with the name of the blueprint.
        """

        def decorator(f):  # pylint:disable=invalid-name
            endpoint = options.pop("endpoint", f.__name__)
            updated_rule = rule

            if version:
                params = dict(prefix=API_PREFIX, version=version, rule=rule)
                if self.api_prefix:
                    pattern = '{prefix}{version}/{api_prefix}{rule}'
                    params['api_prefix'] = self.api_prefix
                else:
                    pattern = '{prefix}{version}{rule}'

                updated_rule = pattern.format(**params)

            self.add_url_rule(updated_rule, endpoint, f, **options)
            return f

        return decorator
