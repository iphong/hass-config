#pragma once

#include <string>
#include <utility>
#include <vector>

#include "esphome/core/automation.h"
#include "esphome/core/base_automation.h"
#include "esphome/core/component.h"
#include "esphome/core/defines.h"

namespace esphome {
namespace esp_net {

class Component : public esphome::Component {
   public:
};

class Subscribe : public Trigger<>, Component {
   public:
	Subscribe(Component* component){};
};

class PublishBase {};

template <typename... Ts>
class Publish : public Action<Ts...>, PublishBase {
   public:
	Publish(Component* component){};
	void play(Ts... x) override{};
};

}  // namespace esp_net
}  // namespace esphome
