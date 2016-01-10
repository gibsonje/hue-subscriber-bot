from formencode import Schema, validators, ForEach

class SchemaMapper:

    def __init__(self, schema, **kwargs):
        """
        :type schema: Schema
        :param schema: Schema of the gui
        :return:
        """

        self.schema = schema
        self.bindings = {}

    def bind(self, schema_uri, set_data, get_data):
        self.bindings[schema_uri] = (set_data, get_data)

    def get_bound(self):
        return {k: v[1]() for k, v in self.bindings.iteritems()}

    def set_bound(self, config):
        """
        Using known bindings, set from each value in the config dict.
        :type config: dict
        :param config: The config dictionary.
        """
        for k, v in self.bindings.iteritems():
            set_data, get_data = v
            field_data = self.get_nested(config, k)
            set_data(field_data)

    def get_nested(self, data, uri, uri_splitter=":"):
        """
        Get a nested value from a dictionary using the specified uri.
        :type data: dict
        :type uri: str
        :type uri_splitter: str
        :param data:
        :param uri:
        :return:
        """
       # {k: d[k] for d, k in uri.split(":")}
        return reduce(lambda d, k: d[k], uri.split(uri_splitter),
                      data)


if __name__ == "__main__":
    class Test2(Schema):
      test = validators.String(if_missing="Bye!")

    class Test(Schema):
        nest = Test2




    data = {'nest': {
        'test': "Hi!"
    }}
    test = SchemaMapper(Test)

    config_python = Test.to_python(data)
    config = Test.from_python(config_python)

    schema_map = SchemaMapper(Test)
    def set_thing(x):
        print x

    def get_thing():
        return "Hello World!"
    schema_map.bind("nest:test", set_thing, get_thing)

    schema_map.set_bound({"nest":{"test": "Blah!"}})





