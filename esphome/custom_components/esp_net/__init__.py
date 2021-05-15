import esphome.codegen as cg
import esphome.config_validation as cv
import esphome.const as ehc
from esphome.core import CORE, coroutine
from esphome.core import coroutine_with_priority
from esphome import automation

esp_net_ns = cg.esphome_ns.namespace('esp_net')

Component = esp_net_ns.class_('Component', cg.Component)
Publish = esp_net_ns.class_('Publish', automation.Action)
Subscribe = esp_net_ns.class_('Subscribe', automation.Trigger, cg.Component)

CODEOWNERS = ["@iphong"]

CONFIG_SCHEMA = cv.All(cv.COMPONENT_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(Component),
    cv.Optional("subscribe"): automation.validate_automation({
        cv.GenerateID(ehc.CONF_TRIGGER_ID): cv.declare_id(Subscribe),
        cv.Optional("topic"): cv.All(cv.string, cv.Length(min=2)),
    }),
}))
PUBLISH_SCHEMA = cv.Schema({
    cv.Optional("topic"): cv.All(cv.string, cv.Length(min=2)),
    cv.Optional("payload"): cv.All(cv.string, cv.Length(min=2)),
})


@automation.register_action("esp_net.publish", Publish, PUBLISH_SCHEMA)
@coroutine
def publish_to_code(config, action_id, template_arg, args):
    component = yield cg.get_variable(CORE.config["esp_net"][ehc.CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, component)
    ActionPtr = Publish.template(template_arg).operator('ptr')
    args = args + [(ActionPtr, 'publish')]
    template_arg = cg.TemplateArguments(*[arg[0] for arg in args])
    yield var

@coroutine
def subscribe_to_code(component, config):
    var = cg.new_Pvariable(config[ehc.CONF_TRIGGER_ID], component)
    yield automation.build_automation(var, [], config)
    yield cg.register_component(var, config)
    yield var

@coroutine_with_priority(1.0)
def to_code(config):
    if CORE.is_esp8266:
        cg.add_library('ESP8266WiFi', None)
    var = cg.new_Pvariable(config[ehc.CONF_ID])
    for conf in config.get("subscribe", []):
        yield subscribe_to_code(var, conf)
    yield cg.register_component(var, config)
    yield var
