<template>
  <div class="tesla-car">
    <div class="tesla-wheels">
      <div :class="`tesla-wheel tesla-wheel--front tesla-wheel--${wheelsize}--${speed}`"></div>
      <div :class="`tesla-wheel tesla-wheel--rear tesla-wheel--${wheelsize}--${speed}`"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppCar',
  props: {
    wheelsize: {
      type: Number,
      required: true
    },
    speed: {
      type: Number,
      required: true
    }
  }
};
</script>